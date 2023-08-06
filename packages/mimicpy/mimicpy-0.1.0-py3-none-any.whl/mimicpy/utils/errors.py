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

"""Module for custom exceptions"""


class MiMiCPyError(Exception):
    """Generic exception from MiMiCPy"""

class SelectionError(MiMiCPyError):
    """Error in selecting atoms in Mpt"""

class ParserError(MiMiCPyError):
    """Error in parsing a file"""
    def __init__(self, file='', file_type='', line_number='', details=''):
        self.file = file
        self.file_type = file_type
        self.line_number = line_number
        self.details = details
        if self.file_type:
            self.file_type = ' as ' + file_type
        if self.line_number:
            self.line_number = ' at line number {}'.format(line_number)
        if self.details:
            self.details = ': ' + details

    def __str__(self):
        return 'Error parsing {}{}{}{}'.format(self.file, self.file_type, self.line_number, self.details)

class ScriptError(MiMiCPyError):
    """Requested parameter does not exist in script object"""
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return 'The {} parameter has not been set correctly'.format(self.parameter)
