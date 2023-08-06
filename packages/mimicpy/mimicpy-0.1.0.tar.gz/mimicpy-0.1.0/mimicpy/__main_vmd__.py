#!/usr/bin/env python

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

import sys
import mimicpy


class MockAtomSel:
    """Class to mock AtomSel class from vmd python module"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            # Tcl returns eveything as space separated strings
            lst = v.split()
            # Convert string to int or float
            if k == 'index':
                lst = [int(i) for i in lst]
            elif k in ['x', 'y', 'z']:
                lst = [float(i) for i in lst]
            setattr(self, k, lst)


class MockVMDModule:
    """
    Class to mock vmd python module
    Results of following Tcl commands to be passed in the constructor:
        ##Values set to TclVMDConnector.sele
        atomsel get name
        atomsel get index
        atomsel get resname
        atomsel get x
        atomsel get y
        atomsel get z
        ##Values set to TclVMDConnector.sele_link
        atomsel get name
        atomsel get index
        atomsel get resname
        atomsel get x
        atomsel get y
        atomsel get z
        ##Values set to TclVMDConnector.box_size
        molinfo <molid> get a
        molinfo <molid> get b
        molinfo <molid> get c
        molinfo <molid> get alpha
        molinfo <molid> get beta
        molinfo <molid> get gamma

    All should be passed in this order. Each param is a space separated string.
    The gro file should be loaded in Tcl/VMD as it will not be loaded here.
    """

    def __init__(self, params):
        if len(params) < 12:
            raise mimicpy.utils.errors.MiMiCPyError("Not enough params passed to TclVMDConnector")
        self.sele = params[:6]
        self.sele_link = params[6:12]
        self.box_size = params[12:]
        self.molecule = type('obj', (object,), {'load' : lambda a, b: -1, 'get_periodic': self.__get_periodic})

    def __get_periodic(self, *args):
        if not self.box_size:
            raise mimicpy.utils.errors.MiMiCPyError("Did not receive system box size information from Tcl")
        box_vals = [float(b) for b in self.box_size]
        box_keys = ['a', 'b', 'c', 'alpha', 'beta', 'gamma']
        # Return as dict of vals like the VMD python module
        return dict(zip(box_keys, box_vals))

    def atomsel(self, selection, *args):
        # Selection params come from Tcl script
        params = ['name', 'index', 'resname', 'x', 'y', 'z']
        if selection == 'link':
            kwargs = dict(zip(params, self.sele_link))
        else:
            kwargs = dict(zip(params, self.sele))
        return MockAtomSel(**kwargs)


class MockVMDSelector(mimicpy.VMDSelector):
    """
    Class to mock VMDSelector class
    Removes requirement of VMD python package, by reading data directly set from Tcl
    """

    def __init__(self, mpt_file, molid, tcl_vmd_params):
        self.molid = molid
        self.cmd = MockVMDModule(tcl_vmd_params)
        self.mpt = mimicpy.Mpt.from_file(mpt_file)


def main():
    if len(sys.argv) < 31:
        print("This program is intented to be used solely by the VMD plugin\n")
        sys.exit(1)

    top = sys.argv[1]
    inp = None if sys.argv[2] == 'None' else sys.argv[2]
    ndx = sys.argv[3]
    out = sys.argv[4]
    molid = sys.argv[5]
    sele_link = None if sys.argv[6] == 'None' else sys.argv[6]
    pad = float(sys.argv[7])
    absl = bool(sys.argv[8] == 'True')
    qma = sys.argv[9]
    path = None if sys.argv[10] == 'None' else sys.argv[10]
    q = None if sys.argv[11] == 'None' else float(sys.argv[11])
    pp = None if sys.argv[12] == 'None' else sys.argv[12]
    find_link = bool(sys.argv[13] == 'True')
    # sys.argv[14:] should have all selection info from VMD

    try:
        qm = mimicpy.Preparation(MockVMDSelector(top, molid, sys.argv[14:]))
    except FileNotFoundError as e:
        print("\nError: Cannot find file {}.\n".format(e.filename))
        sys.exit(1)
    except (mimicpy.utils.errors.ParserError, mimicpy.utils.errors.MiMiCPyError) as e:
        print(e)
        sys.exit(1)

    try:
        qm.add('not link')
    except mimicpy.utils.errors.MiMiCPyError as e:
        print(e)
        sys.exit(1)

    if sele_link is not None:
        try:
            qm.add('link', is_link=True)
        except mimicpy.utils.errors.MiMiCPyError as e:
            print(e)
            sys.exit(1)
    elif find_link:
        qm.find_link_atoms()
        print("Link atoms added automatically.")

    try:
        qm.get_mimic_input(inp, ndx, out, pad, absl, qma, path, q, pp)
    except FileNotFoundError as e:
        print("\nError: Cannot find file {}.\n".format(e.filename))
        sys.exit(1)
    except mimicpy.utils.errors.SelectionError as e:
        print(e)

if __name__ == '__main__':
    main()
