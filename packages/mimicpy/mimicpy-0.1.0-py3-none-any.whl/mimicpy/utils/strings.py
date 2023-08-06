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

import re

def clean(txt, comments=None):
    if comments:  # Can be single string or a list of strings
        if isinstance(comments, str):
            comments = [comments]
        for c in comments:
            txt = re.sub(re.compile(str(c)+r"(.*)\n" ) ,"\n" , txt)  # Strip comments
    return re.sub(re.compile(r"[\n]+"), "\n", txt)

def print_table(dct, printer):
    # get length of largest entry in each col
    cols = dct.keys()
    n = [len(c)+1 for c in cols]

    for i,c in enumerate(cols):
        for j in dct[c]:
            if n[i] < len(j)+1: n[i] = len(j)+1


    template = "| " + "| ".join(["{:^" + str(i) + "}" for i in n]) + "|"

    dashes = '-'*(sum(n)+2*len(n)-1)

    printer("+{}+".format(dashes))
    printer(template.format(*cols))
    printer("+{}+".format(dashes))

    vals = dct.values()
    lst = list(map(list, zip(*vals))) # transpose list

    for i in lst:
        printer(template.format(*i))
        printer("+{}+".format(dashes))

def print_dict(dct, col1, col2, printer):
    new_dct = {col1: list(dct.keys()), col2: list(dct.values())}
    print_table(new_dct, printer)
