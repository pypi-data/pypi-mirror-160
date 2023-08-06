# MiMiCPy
MiMiCPy is the companion library to MiMiC QM/MM package. It comes with a set of command lines tools to prepare MiMiC input scripts. Additionally, plugins for PyMOL and VMD are also provided.

## Installation
To install, run the following command:

pip install mimicpy

Or clone the source repo and install using ```setup.py``` in the root folder.
```
pip install git+https://gitlab.com/MiMiC-projects/mimicpy
```
Here ```mimicpy/``` is the directory to which this repo was cloned to.

To install with PyMOL and/or VMD support, pass the plugin path to ```PYMOLDIR``` or ```VMDDIR```. This path is usually either the path to PyMOL/VMD installation folder, or the user home directory. For example,
```
PYMOLDIR="/home/user/" VMDDIR="/home/user/" pip install mimicpy
```

## Portability Issues
MiMiCPy requires Python >= 3.5, pandas >= 0.24.0 and numpy >= 1.12.0. The plugins have been tested with PyMOL version 2.3.4 and VMD version 1.9.4a38, although other versions are expected to work. If any incompatibilities are found, please post an issue on GitLab.

## Demo
A demo of atom selection for the QM region, and generation of the CPMD-MiMiC input script using MiMiCPy is shown below.
```console
user@system:~$ mimicpy prepqm -top acetone.top -coords acetone.gro


 	                ***** MiMiCPy *****

 	 For more information type mimicpy [subcommand] --help

=====> Running prepqm <=====


**Reading topology**

Cannot find path to Gromacs installation.
Read atoms from acetone.itp.
No atoms found in acetone.top.

Some atom types had no atom numbers information.
They were guessed as follows:

+---------------------+
| Atom Type | Element |
+---------------------+
|     c     |    C    |
+---------------------+
|     c3    |    C    |
+---------------------+
|     o     |    O    |
+---------------------+
|     hc    |    H    |
+---------------------+

**Reading coordinates**  |Done

Please enter selection below. For more information type 'help'
> add resname is ACT
> q
Using default values for maxstep and timestep
Wrote Gromacs index file to index.ndx
Wrote new CPMD input script to cpmd.inp

=====> Done <=====

```

For more details and options please refer to the documentation.
