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

"""Module for top files"""

import logging
from os import environ
from os.path import basename, join, isfile
from .itp import Itp
from .topol_dict import TopolDict
from ..utils.errors import MiMiCPyError, ParserError
from ..utils.strings import print_dict
from ..utils.atomic_numbers import atomic_numbers
from ..utils.file_handler import read, write


class Top:
    """reads top files"""

    def __init__(self,
                 file, mode='r',
                 buffer=1000,
                 nonstandard_atomtypes=None,
                 guess_elements=True,
                 gmxdata=None):

        self.file = file
        self.mode = mode
        self.buffer = buffer
        self.nonstandard_atomtypes = nonstandard_atomtypes
        self.guess_elements = guess_elements

        if gmxdata is None:
            if 'GMXDATA' in environ:
                gmxdata = join(environ['GMXDATA'], 'top')
            elif 'GMXLIB' in environ:
                gmxdata = join(environ['GMXLIB'], 'top')

        self.gmxdata = gmxdata

        if self.gmxdata:
            logging.debug('Using {} as path to GROMACS installation'.format(self.gmxdata))
        else:
            self.gmxdata = ''
            logging.warning('Cannot find path to GROMACS installation')

        self.molecules = None
        self.bonds = None
        self.topol_dict = None

        if mode == 'r':
            self.__read()
        elif mode == 'w':
            self.__read(get_atomtypes=True)
        else:
            raise MiMiCPyError('{} is not a mode. Only r or w can be used'.format(mode))

    def __read(self, get_atomtypes=False):
        """Read molecule and atom information"""

        top = Itp(self.file, mode='t', gmxdata=self.gmxdata)
        atom_types = top.atom_types
        if get_atomtypes:
            self.atomtypes = top.atom_types_df
        else:
            self.atomtypes = None
        molecule_types = top.molecule_types

        if self.nonstandard_atomtypes is not None:
            atom_types.update(self.nonstandard_atomtypes)

        atoms = {}
        guessed_elems_history = {}

        for itp_file in top.topology_files:
            itp_file_name = basename(itp_file)
            try:
                itp = Itp(itp_file,
                          molecule_types,
                          atom_types,
                          self.buffer,
                          'r',
                          self.guess_elements,
                          self.gmxdata)
                if itp.topol is not None:
                    atoms.update(itp.topol)
                    guessed_elems_history.update(itp.guessed_elems_history)
                    logging.debug('Read atoms from %s.', itp_file_name)
                else:
                    logging.debug('No atoms found in %s.', itp_file_name)
            except OSError:
                logging.warning('Could not find %s in local or GROMACS data directory. Skipping.', itp_file_name)
        topol_dict = TopolDict.from_dict(atoms)

        self.molecules = top.molecules
        self.bonds = top.bonds
        self.topol_dict = topol_dict

        mols_not_in = self.topol_dict.check_mols(self.molecules)

        if mols_not_in:
            raise ParserError(file=self.file, file_type='GROMACS topology',
                            details="{} defined in the [ molecules ] section did not have corresponding [ atoms ] definition(s)".format(
                                ", ".join(mols_not_in)))
        if guessed_elems_history:
            logging.warning('\nSome atom types had no atom number information.\nThey were guessed as follows:\n')
            print_dict(guessed_elems_history, "Atom Type", "Element", logging.warning)

    def write_atomtypes(self, file, delete_atomtypes=None):
        if self.mode != 'w':
            self.mode = 'w'
            self.__read(True)

        elements = {}
        for k, df in self.topol_dict.todict().items():
            elements.update(dict(zip(df['type'], df['element'])))
        elements = {k:atomic_numbers[v] for k,v in elements.items()}

        itp_str = "; Created by mimicpy fixtop\n[ atomtypes ]\n"
        itp_str += ";  {:^11}{:^6}{:^10}{:^10}{:^6}     {}     {}\n".format('name','at.num','mass','charge','ptype',
                                                                           'sigma','epsilon')
        for i, row in self.atomtypes.iterrows():
            lst = [row[c] for c in self.atomtypes.columns]
            if lst[0] in elements:
                lst[1] = elements[lst[0]]
            else:
                lst[1] = int(lst[1])
            itp_str += "{:>11}{:6d}{:11.4f}{:11.4f}{:>6}     {:e}     {:e}\n".format(*lst)

        import re
        r = re.compile(r"(\[\s*atomtypes\s*\]\n(?:.+\n)+?)\s*(?:$|\[|#)", re.MULTILINE)

        if delete_atomtypes is not None:
            for i in delete_atomtypes:
                txt = read(i)
                atm_typs = r.findall(txt)
                for j in atm_typs:
                    txt = txt.replace(j, '')
                write(txt, i)
            logging.info('Deleted atomtypes sections from %s', ', '.join(delete_atomtypes))

        if isfile(file):
            txt = read(file)
            atm_typs = r.findall(txt)
            if atm_typs != []:
                write(txt.replace(atm_typs[0], itp_str), file)
                logging.info('Fixed and replaced [ atomtypes ] section in %s', file)
            else:
                raise FileExistsError('%s exists and has no [ atomtypes ] section to replace', file)
        else:
            write(itp_str, file)
            logging.info('Fixed [ atomtypes ] section and wrote to %s', file)
