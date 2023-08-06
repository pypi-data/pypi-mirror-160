#
#    MiMiCPy: Python Based Tools for MiMiC
#    Copyright (C) 2020-2021 Bharath Raghavan,
#                            Florian Schackert
#
#    This file is part of MiMiCPy.
#
#    MiMiCPy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    MiMiCPy is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import logging
import pandas as pd
from ..topology.mpt import Mpt
from ..scripts.mdp import Mdp
from ..scripts.ndx import Ndx
from ..scripts.cpmd import CpmdScript, Pseudopotential, Section
from ..utils.errors import SelectionError, MiMiCPyError
from ..utils.constants import BOHR_RADIUS
from ..utils.file_handler import write
from ..utils.strings import print_dict


class Preparation:

    def __init__(self, selector):
        self.__qm_atoms = pd.DataFrame()
        self.selector = selector

    @property
    def qm_atoms(self):
        return self.__qm_atoms

    @staticmethod
    def __clean_qdf(qdf):
        columns = Mpt.columns.copy()
        columns.extend(['x', 'y', 'z'])
        columns_to_drop = [l for l in qdf.columns if l not in columns]
        qdf.index = qdf.index.set_names(['id'])
        return qdf.drop(columns_to_drop, axis=1)

    def add(self, selection=None, is_link=False):
        qdf = Preparation.__clean_qdf(self.selector.select(selection))
        qdf.insert(2, 'is_link', [int(is_link)]*len(qdf))
        self.__qm_atoms = self.__qm_atoms.append(qdf)

    def delete(self, selection=None):
        qdf = Preparation.__clean_qdf(self.selector.select(selection))
        self.__qm_atoms = self.__qm_atoms.drop(qdf.index, errors='ignore')

    def clear(self):
        self.__qm_atoms = pd.DataFrame()

    def find_link_atoms(self):
        bonds = self.selector.mpt.bonds
        qm_atoms = list(self.__qm_atoms.reset_index()['id']) # list of qm atom indices
        qm_bonds = bonds[bonds['atom_i'].isin(qm_atoms) | bonds['atom_j'].isin(qm_atoms)] # list of bonds in which at least one qm atom is involved
        qmmm_link_bonds = qm_bonds[~qm_bonds['atom_i'].isin(qm_atoms) | ~qm_bonds['atom_j'].isin(qm_atoms)] # list of bonds between qm and mm atoms only

        if qmmm_link_bonds.empty:
            logging.info('No QM-MM bonds found! Skipping marking atoms as link')
            return

        linked_atoms = qmmm_link_bonds.to_numpy().flatten() # flatten the above list to a 1D list
        link_qm_atoms = set([a for a in linked_atoms if a in qm_atoms]) # select only qm atoms in the list, and make it unique
        printer = {}

        # set these atoms as link atoms in the qm dataframe
        for link_qm_atom_id in link_qm_atoms:
            self.__qm_atoms.at[link_qm_atom_id ,'is_link'] = int(True)
            key = "{} {}".format(link_qm_atom_id, self.__qm_atoms['name'][link_qm_atom_id])
            val = "{} {}".format(self.__qm_atoms['resid'][link_qm_atom_id], self.__qm_atoms['resname'][link_qm_atom_id])
            printer[key] = val

        logging.info('\nLink atoms were automatically set. The following atoms were marked as link:\n')
        print_dict(printer, "Atom", "Residue", logging.info)

    def get_mimic_input(self,
                        inp_tmp=None,
                        ndx_out=None,
                        inp_out=None,
                        box_padding=0.0,
                        cell_as_absolute=False,
                        ndx_group_name='QMatoms',
                        path=None,
                        charge=None,
                        pp_info=None):
        """Args:
            inp_tmp: cpmd input file, template
            ndx_out: gromacs index file, output
            inp_out: mimic cpmd input file, output
            box_padding: extra distance between qm atoms and wall in nm
            cell_as_absolute: return qm cell info as absolute instead of realtive
            ndx_group_name: name of qmatoms group in the index file
            path: path in the mimic section, overrides template
            charge: charge of the qm region, ovverrides default algorithm
            pp_info: pseudopotential information, pd DataFrame or whitespace separated file
        """

        def qm_cell():
            dims = [0, 0, 0]
            for i, r in enumerate(['x', 'y', 'z']):
                dims[i] = (abs(max(self.__qm_atoms[r]) - min(self.__qm_atoms[r]))
                           + 2 * box_padding) / BOHR_RADIUS
            a, b, c = dims
            if a == 0:
                a = 1 # prevent divide by 0 error
            if not cell_as_absolute:
                b /= a
                c /= a
            cell = ' '.join((str(round(a, 1)), str(round(b, 1)), str(round(c, 1)), '0.0 0.0 0.0'))
            return cell

        # handle pp_info dataframe
        if pp_info is None:
            pp_info = pd.DataFrame()
        elif isinstance(pp_info, str):
            pp_info_file_name = pp_info
            pp_info = pd.read_csv(pp_info_file_name,
                                  header=None,
                                  names=['element','pp_name','pp_link_name','labels','lmax','loc'],
                                  delim_whitespace=True,
                                  comment='#')
            pp_info = pp_info.set_index('element')
            pp_info = pp_info.drop_duplicates(keep='first')

        if pp_info.isna().any().any():
            raise MiMiCPyError('Missing information in {}'.format(pp_info_file_name))

        def get_pp_info(element, is_link):
            default_pp_name = lambda : element + '_MT_BLYP_LINK.psp' if is_link else element + '_MT_BLYP.psp'

            try:
                pp_name = str(pp_info.loc[element]['pp_link_name']) if is_link else str(pp_info.loc[element]['pp_name'])
                labels = str(pp_info.loc[element]['labels'])
                lmax = str(pp_info.loc[element]['lmax'])
                loc = str(pp_info.loc[element]['loc'])

                if lmax == '-': lmax = 'S'
                if loc == '-': loc = ''
                if labels == '-': labels = ''
                if pp_name == '-': pp_name = default_pp_name()

                return pp_name, labels, lmax, loc
            except KeyError:
                return default_pp_name(), 'KLEINMAN-BYLANDER', 'S', ''

        # Check for obvious errors in selection
        if self.__qm_atoms.empty:
            raise SelectionError('No atoms have been selected for the QM partition')

        # Create an index group in GROMACS format (and write it to a file)
        qm_ndx_group = Ndx(ndx_group_name)
        setattr(qm_ndx_group, ndx_group_name, self.__qm_atoms.index.to_list())
        if ndx_out:
            write(str(qm_ndx_group), ndx_out, 'w')
            logging.info('Wrote Gromacs index file to %s', ndx_out)

        # Create CPMD input script
        sorted_qm_atoms = self.__qm_atoms.sort_values(by=['is_link', 'element']).reset_index()

        if inp_tmp is None:
            cpmd = CpmdScript('MIMIC', 'CPMD', 'SYSTEM', 'ATOMS')
        elif isinstance(inp_tmp, str):
            cpmd = CpmdScript.from_file(inp_tmp)
        else:
            cpmd = inp_tmp

        if not cpmd.has_parameter('MIMIC'):
            cpmd.MIMIC = Section()
        if not cpmd.has_parameter('CPMD'):
            cpmd.CPMD = Section()
        if not cpmd.has_parameter('SYSTEM'):
            cpmd.SYSTEM = Section()
        cpmd.ATOMS = Section()

        # Get overlaps and atoms
        overlaps = '{}'.format(len(sorted_qm_atoms))
        for i, atom in sorted_qm_atoms.iterrows():
            gromacs_id = atom['id']
            cpmd_id = i + 1
            overlaps += '\n2 {} 1 {}'.format(gromacs_id, cpmd_id)
            pp_name, labels, lmax, loc = get_pp_info(str(atom['element']), atom['is_link'])
            coords = [atom['x']/BOHR_RADIUS, atom['y']/BOHR_RADIUS, atom['z']/BOHR_RADIUS]
            if cpmd.ATOMS.has_parameter(pp_name):
                pp_block = getattr(cpmd.ATOMS, pp_name)
                pp_block.coords.append(coords)
            else:
                setattr(cpmd.ATOMS, pp_name, Pseudopotential(coords, labels, lmax, loc))
        cpmd.MIMIC.OVERLAPS = overlaps

        if path:
            from pathlib import Path
            cpmd.MIMIC.PATHS = '1\n' + str(Path(os.path.expanduser(path)).resolve())
        elif not cpmd.MIMIC.has_parameter('paths'):
            cpmd.MIMIC.PATHS = '1\n' + str(os.getcwd())
        cpmd.MIMIC.BOX = ' '.join([str(s/BOHR_RADIUS) for s in self.selector.mm_box])

        cpmd.CPMD.MIMIC = True

        cell = qm_cell()
        if cell_as_absolute:
            cpmd.SYSTEM.CELL__ABSOLUTE = cell
            cpmd.SYSTEM.CELL = None
        else:
            cpmd.SYSTEM.CELL = cell
            cpmd.SYSTEM.CELL_ABSOLUTE = None

        if charge:
            cpmd.SYSTEM.CHARGE = charge
        else:
            total_charge = sum(self.__qm_atoms['charge'])
            if not round(total_charge, 2).is_integer():
                logging.warning('Total charge of QM region is %s, Rounding to integer',
                                total_charge)
            cpmd.SYSTEM.CHARGE = round(total_charge)

        if inp_out is None:
            logging.info('Created new CPMD input script for MiMiC run')
        else:
            write(str(cpmd), inp_out, 'w')
            logging.info('Wrote new CPMD input script to %s', inp_out)

        return qm_ndx_group, cpmd

    @staticmethod
    def get_gmx_input(inp=None, qmatoms='QMatoms', out=None):

        if inp is None:
            mdp = Mdp()
        elif isinstance(inp, str):
            mdp = Mdp.from_file(inp)
        else:
            mdp = inp

        errors = False
        if (not mdp.has_parameter('integrator') or mdp.integrator != 'mimic') and inp is not None:
            logging.warning('Wrong integrator for a MiMiC run, setting integrator = mimic')
            errors = True
        if (not mdp.has_parameter('QMMM_grps') or mdp.QMMM_grps != qmatoms) and inp is not None:
            logging.warning('QM atoms index group name and QMMM-grps parameter do not correspond, setting QMMM-grps = %s', qmatoms)
            errors = True
        if mdp.has_parameter('constraints') and mdp.constraints != 'none':
            logging.warning('Molecules should not be constrained by GROMACS, setting constraints = none')
            errors = True
        if mdp.has_parameter('tcoupl') and mdp.tcoupl != 'no':
            logging.warning('Temperature coupling will not be activated by GROMACS, setting tcoupl = no')
            errors = True
        if mdp.has_parameter('pcoupl') and mdp.pcoupl != 'no':
            logging.warning('Pressure coupling will not be activated by GROMACS, setting pcoupl = no')
            errors = True
        if mdp.has_parameter('dt'):
            dt = float(mdp.dt)
            if dt > 0.0001:
                logging.warning('Timestep may be too large for grompp, setting dt = 0.0001')
                errors = True

        mdp.integrator = 'mimic'
        mdp.qmmm_grps = qmatoms
        mdp.constraints = 'none'
        mdp.tcoupl = 'no'
        mdp.pcoupl = 'no'
        mdp.dt = 0.0001

        if not errors and inp is not None:
            if isinstance(inp, str):
                fname = inp
            else:
                fname = 'MDP script'
            logging.info('No errors found in %s', fname)
        elif out is None:
            logging.info('Created new MDP script for MiMiC run')
        else:
            write(str(mdp), out, 'w')
            logging.info('Wrote fixed MDP script to %s', out)

        return mdp
