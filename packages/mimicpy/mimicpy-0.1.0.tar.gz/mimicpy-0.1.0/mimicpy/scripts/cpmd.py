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

"""Module for CPMD input scripts"""

import re
import numpy as np
import pandas as pd
from .script import Script
from ..coords.base import CoordsIO
from ..utils.strings import clean
from ..utils.errors import ParserError, MiMiCPyError
from ..utils.constants import BOHR_RADIUS


class Pseudopotential:
    """formats pseudopotential blocks in the ATOMS section"""

    def __init__(self, coords, labels='KLEINMAN-BYLANDER', lmax='S', loc=''):
        self.coords = coords if all(isinstance(i, list) for i in coords) else [coords]
        self.labels = labels
        self.lmax = lmax
        self.loc = loc

    def __str__(self):
        if not self.labels.startswith(' ') and self.labels != '':
            self.labels = ' ' + self.labels

        pp_block = '{}\n'.format(self.labels)
        pp_block += '    LMAX={}'.format(self.lmax)
        pp_block += '\n' if (self.loc == '' or self.loc == self.lmax) else ' LOC={}\n'.format(self.loc)
        pp_block += '    {}\n'.format(len(self.coords))

        for row in self.coords:
            pp_block += ' {:>18.12f} {:>18.12f} {:>18.12f}\n'.format(row[0], row[1], row[2])

        return pp_block

    @classmethod
    def from_string(cls, string):
        splt = string.splitlines()
        labels = splt[0].strip()

        second_line_regex = re.compile(r'(\w+)\s*=\s*(\w)')
        second_line = dict(second_line_regex.findall(splt[1]))
        if 'LMAX' in second_line:
            lmax = second_line['LMAX']
        else:
            raise ParserError(file='CPMD script', details='no LMAX data for pseudopotential')
        if 'LOC' in second_line:
            loc = second_line['LOC']
        else:
            loc = ''

        number_of_atoms = int(splt[2].strip())
        string_to_list = lambda string: [float(i) for i in string.split()]
        coords = [string_to_list(i) for i in splt[3:]]
        if len(coords) != number_of_atoms:
            raise ParserError(file='CPMD script', details='mismatch in number of atoms ({} vs {})'.format(number_of_atoms, len(coords)))

        return cls(coords, labels, lmax, loc)


class Section(Script):
    """formats sections in a CPMD input script"""

    def __str__(self):
        section_string = ''
        for keyword in self.parameters:
            value = getattr(self, keyword)
            if value is None:
                continue
            if isinstance(value, Pseudopotential):
                section_string += '\n*{}{}'.format(keyword, str(value))
            else:
                section_string += '\n    {}'.format(keyword.replace('__', ' ').replace('_', '-'))
                if keyword == 'OVERLAPS':
                    value = '\n'.join(['        '+s.strip() for s in value.splitlines()])
                    section_string += '\n{}'.format(str(value))
                elif value is not True:
                    section_string += '\n        {}'.format(str(value))
        return section_string

    @staticmethod
    def __is_numeric(string):
        splt = string.split()
        if len(splt) == 1:
            return string.replace('.','').replace('-','').isnumeric()
        for i in splt:
            if not Section.__is_numeric(i):
                return False
        return True

    @classmethod
    def from_string(cls, string):
        i = 0
        section = cls()
        splt = string.splitlines()

        if len(splt) == 1:
            setattr(section, splt[0].strip(), True)

        while i < len(splt):
            splt_i = splt[i].strip()

            if splt_i == 'PATHS':
                try:
                    setattr(section, splt_i, "\n".join([s.strip() for s in splt[i+1:i+3]]))
                except IndexError as e:
                    raise ParserError(file='CPMD script', details='PATHS in MIMIC section not formatted correctly') from e
                i += 2

            elif splt_i == 'OVERLAPS':
                try:
                    number_of_overlaps = int(splt[i+1])
                    overlaps = "\n".join([s.strip() for s in splt[i+1:i+number_of_overlaps+2]])
                except IndexError as e:
                    raise ParserError(file='CPMD script', details='OVERLAPS in MIMIC section not formatted correctly') from e
                setattr(section, splt_i, overlaps)
                i += number_of_overlaps + 1

            elif splt_i.startswith('*'):  # Take care of pseudopotentials
                pp_file = splt_i.split()[0][1:]
                labels = splt_i.split()[1]
                lmax_loc = splt[i+1]
                number_of_atoms = int(splt[i+2])
                coords = splt[i+3:i+3+number_of_atoms]

                pp_string =  labels + '\n'
                pp_string += lmax_loc + '\n'
                pp_string += str(number_of_atoms) + '\n'
                pp_string += '\n'.join([str(xyz) for xyz in coords])

                setattr(section, pp_file, Pseudopotential.from_string(pp_string))
                i += number_of_atoms + 1

            elif i < len(splt)-1 and Section.__is_numeric(splt[i+1].strip()):
                setattr(section, splt_i, splt[i+1].strip())
                i += 1

            elif not Section.__is_numeric(splt[i]):
                setattr(section, splt_i, True)
            i += 1

        return section


class CpmdScript(Script):
    """formats CPMD input scripts and writes coordinates to a file"""

    def __init__(self, *sections):
        super().__init__()
        for section in sections:
            setattr(self, section, Section())

    def __str__(self):
        cpmd_script = ''
        for section in self.parameters:
            section_string = str(getattr(self, section))
            cpmd_script += '\n&{}{}\n&END\n'.format(section, section_string)
        return cpmd_script

    @classmethod
    def from_string(cls, string):
        string = clean(string)
        section_reg = re.compile(r'\s*\&(.*?)\n((?:.+\n)+?)\s*(?:\&END)')
        sections = section_reg.findall(string)

        inp = cls()
        for key, value in sections:
            setattr(inp, key, Section.from_string(value))
        return inp

    def to_coords(self, mpt, out, title=None, ext=None):
        if not title:
            title = 'Coordinates from CPMD/MiMiC script'
        if not self.has_parameter('ATOMS'):
            raise MiMiCPyError('No ATOMS section found in CPMD script')
        if not self.has_parameter('MIMIC'):
            raise MiMiCPyError('MIMIC section not found in CPMD script')
        if not self.MIMIC.has_parameter('OVERLAPS'):
            raise MiMiCPyError('OVERLAPS not found in MIMIC section')

        try:
            ids = [int(i.split()[1]) for i in self.MIMIC.OVERLAPS.splitlines()[1:]]
        except (ValueError, IndexError) as e:
            raise ParserError(file='CPMD script', details='OVERLAPS in MIMIC section not formatted correctly') from e

        coords = []
        for pseudopotential in self.ATOMS.parameters.values():
            coords += pseudopotential.coords
        coords = np.array(coords)*BOHR_RADIUS

        if len(ids) != coords.shape[0]:
            raise MiMiCPyError('Mismatch between number of atoms in OVERLAPS and ATOMS sections ({} vs {})'.format(len(ids), coords.shape[0]))
        coords = pd.DataFrame({'id': ids, 'x': coords[:,0], 'y': coords[:,1], 'z': coords[:,2]})

        CoordsIO(out, mode='w', ext=ext).write(mpt, coords, title=title)
