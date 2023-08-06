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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Module for pdb files"""

import pandas as pd
from .base import BaseCoordsClass

class Pdb(BaseCoordsClass):
    """Reads  and writes PDB files
       File Format taken from:
           https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html
    """
            
    def __read_line(self, line):
        vals = {}
        vals['record'] = line[:6].strip()

        if vals['record'] != 'HETATM' and vals['record'] != 'ATOM':
            vals['content'] = line[6:]
            return vals
        
        def cnvto(a, type):
            try:
                return type(a)
            except:
                return a
                
        vals['id'] = cnvto(line[6:11].strip(), int)
        vals['name'] = line[12:16].strip()
        vals['altLoc'] = line[16]
        vals['resname'] = line[17:20].strip()
        vals['chainID'] = line[21]
        vals['resSeq'] = cnvto(line[22:26].strip(), int)
        vals['iCode'] = line[26]
        vals['x'] = float(line[30:38].strip())
        vals['y'] = float(line[38:46].strip())
        vals['z'] = float(line[46:54].strip())
        vals['occupancy'] = cnvto(line[54:60].strip(), float)
        vals['tempFactor'] = cnvto(line[60:66].strip(), float)
        vals['element'] = line[76:78].strip()
        vals['charge'] = cnvto(line[78:80].strip(), float)

        return vals

    def _read(self):
        # ATOM/HETATM line is always 78 bytes/chars
        self.file.buffer = 78*self.buffer

        pdb_lst = []

        for chunk in self.file:

            for line in chunk.splitlines():
                try:
                    vals = self.__read_line(line)
                except: # if only part of line was read
                    self.file.file.seek(-len(line), 1) # push back the file pointer to start of line

                if vals['record'] == 'ATOM' or vals['record'] == 'HETATM':
                    pdb_lst.append(vals)

        coords = pd.DataFrame(pdb_lst)

        dims = [0, 0, 0]
        for i, r in enumerate(['x', 'y', 'z']):
            coords[r] /= 10 # convert ang to nm
            dims[i] = abs(max(coords[r]) - min(coords[r])) # find box size
        
        return coords, dims

    def _write(self, mpt_coords, box, title):
        def guess_chain(s):
            """Guess chain ID from molecule name
               It is not very accurate
            """
            try:
                chain = [l for l in s if l.isupper()][-1]
            except IndexError:
                chain = ' '
            
            if chain not in ['A', 'B', 'C', 'D']:
                chain = ' '
            
            return chain
        
        def name_checker(s):
            s = self.str_checker(s, 4)
            if len(s) == 3:
                return " {}".format(s)
            else:
                return "{:^4}".format(s)
       
        def charge_checker(i):
            i = round(i)
            if i>0:
                return "{}+".format(i)
            elif i<0:
                return "{}-".format(-i)
            else:
                return "  "
        
        std_res = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'HID', 'ILE', 'LEU', 'LYS',
                   'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
        
        pdb_str = ''
        for i, r in mpt_coords.iterrows():
            resname = r['resname'].upper()
            if resname in std_res:
                record = 'ATOM'
            else:
                record = 'HETATM'
            
            pdb_str += '{:<6}{:>5d} {} {:>3} {:1}{:>4d}    {:>8.3f}{:>8.3f}{:>8.3f}  0.00  0.00          {:>2}{}\n'.format(record,\
                                                                        self.int_checker(r['id'], 5),\
                                                                        name_checker(r['name']),\
                                                                        self.str_checker(resname, 3),\
                                                                        guess_chain(r['mol']),\
                                                                        self.int_checker(r['resid'], 4),\
                                                                        r['x']*10,\
                                                                        r['y']*10,\
                                                                        r['z']*10,\
                                                                        self.str_checker(r['element'], 2),\
                                                                        charge_checker(r['charge'])
                                                                       )
        pdb_str += "TER   \n"
        
        if box is None:
            box = [0, 0, 0]
            for i, c in enumerate(['x', 'y', 'z']):
                box[i] = abs(max(mpt_coords[c]*10) - min(mpt_coords[c]*10)) # find box size
        
        if title:
            title = "TITLE     {}\n".format(title.upper())
        header = ("{}REMARK    GENERATED BY MIMICPY\n"
                  "CRYST1{:9.3f}{:9.3f}{:9.3f}{:7.3f}{:7.3f}{:7.3f} P 1           1\n".format(title, box[0], box[1], box[2], 90, 90, 90))
        
        return header+pdb_str
