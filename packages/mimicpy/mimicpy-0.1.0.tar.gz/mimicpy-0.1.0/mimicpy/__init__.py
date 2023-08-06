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

import logging
from ._version import __version__
from ._authors import __authors__
from mimicpy.core.prepare import Preparation
from mimicpy.core.selector import DefaultSelector, VMDSelector, PyMOLSelector
from mimicpy.topology.mpt import Mpt
from mimicpy.topology.top import Top
from mimicpy.scripts.mdp import Mdp
from mimicpy.scripts.cpmd import CpmdScript
from mimicpy.scripts.ndx import Ndx
from mimicpy.coords.base import CoordsIO
from mimicpy.coords.gro import Gro
from mimicpy.coords.pdb import Pdb

logging.basicConfig(format='%(message)s',
                    filemode='w',
                    level=logging.INFO)