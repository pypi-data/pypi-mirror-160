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

"""Module for MiMiCPy-specific molecule:topology dictionary"""


class TopolDict:
    """provides a dictionary with non-repeating topology information"""

    @classmethod
    def from_dict(cls, dict_df):
        keys = list(dict_df.keys())
        repeating = {}
        i = 0
        while i < len(keys):
            key_i = keys[i]
            for j in range(i+1, len(keys)):
                key_j = keys[j]
                if dict_df[key_i].equals(dict_df[key_j]):
                    repeating[key_j] = key_i
                    del dict_df[key_j]
            i += 1
            keys = list(dict_df.keys())
        return cls(dict_df, repeating)

    def __init__(self, dict_df, repeating):
        self.dict_df = dict_df
        self.repeating = repeating

    def __getitem__(self, key):
        if key in self.dict_df:
            return self.dict_df[key]
        if key in self.repeating:
            return self.dict_df[self.repeating[key]]
        raise KeyError('Molecule {} is not in topology'.format(key))

    def __contains__(self, key):
        return key in self.dict_df or key in self.repeating

    def todict(self):
        extras = self.dict_df.copy()
        for i in self.repeating:
            extras[i] = self.__getitem__(i)
        return extras

    def __str__(self):
        return str(self.todict())

    def __repr__(self):
        return repr(self.todict())

    def keys(self):
        """Handle keys of a TopolDict like keys of a regular dict"""
        combined_dict = self.dict_df.copy()
        combined_dict.update(self.repeating)
        all_keys = combined_dict.keys()
        return all_keys

    def check_mols(self, mols):
        return list(set([mol[0] for mol in mols if mol[0] not in self]))
