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

"""Module for abstract script class"""

from collections import OrderedDict
from abc import ABC, abstractmethod
from ..utils.errors import ScriptError
from ..utils.file_handler import read


class Script(ABC):
    """stores internal attributes in a dictionary and script parameters in an ordered dictionary"""

    def __init__(self):
        self.__orddict__ = OrderedDict()

    @property
    def parameters(self):
        return self.__orddict__

    def has_parameter(self, parameter):
        return bool(parameter in self.__orddict__)

    def clear_parameters(self):
        self.__orddict__ = OrderedDict()

    def __setattr__(self, key, value):
        if key.startswith('_') or key in ['parameters', 'has_parameter', 'clear_parameters']:
            # Private attributes and helper functions are stored in __dict__
            self.__dict__[key] = value
        else:
            # All others are script parameters and stored in __orddict__
            self.__orddict__[key.replace(' ', '--').replace('-', '_')] = value

    def __getattr__(self, key):
        if key.startswith('_') or key in ['parameters', 'has_parameter', 'clear_parameters']:
            return self.__getattribute__('__dict__')[key]
        try:
            return self.__getattribute__('__orddict__')[key]
        except KeyError as key_error:
            raise ScriptError(key) from key_error

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    @classmethod
    @abstractmethod
    def from_string(cls, string):
        pass

    @classmethod
    def from_file(cls, file):
        if isinstance(file, Script):
            return file
        return cls.from_string(read(file, 'r'))
