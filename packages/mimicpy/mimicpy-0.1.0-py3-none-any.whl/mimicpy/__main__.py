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
from os.path import isfile
import time
import argparse
import readline
import warnings
import itertools
import threading
import pandas as pd
import mimicpy

warnings.simplefilter(action='ignore', category=FutureWarning)  # Supress pandas warnings


class Loader:

    def __init__(self, message):

        self.done = False
        self.message = message
        t = threading.Thread(target=self.__animate)
        t.start()

    def __animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write('\r{}  '.format(self.message) + c)
            sys.stdout.flush()
            time.sleep(0.1)

    def close(self, halt=False):
        self.done = True
        if not halt:
            print('Done')

# TODO: Unify the three helper functions
def __str2bool(string):
    if isinstance(string, bool):
        return string
    if string.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if string.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        print('Error! boolean value expected for argument\n')
        sys.exit(1)

def __str2float(v):
    if v is not None:
        try:
            return float(v)
        except:
            print('Error! float value expected for argument\n')
            sys.exit(1)
    else:
        return 0.0

def __str2int(v):
    try:
        return int(v)
    except:
        print('Error! integer value expected for argument\n')
        sys.exit(1)

def prepqm(args):

    def selection_help():
        print("\nvalid subcommands:\n\n"
              "    o add       <selection>    add selected atoms to QM region\n"
              "    o add-link  <selection>    add selected atoms to QM region as link atoms\n"
              "    o delete    <selection>    delete selected atoms from QM region\n"
              "    o clear                    clear all atoms from QM region\n"
              "    o view      <file-name>    print current QM region to console or file\n"
              "    o quit                     create CPMD input and GROMACS index files and quit\n"
              "    o help                     show this help message\n\n"
              "For more information on the selection langauge please refer to the docs.\n")

    def view(file_name=None):
        if prep.qm_atoms.empty:
            print("No QM atoms have been selected")
        else:
            # display whole dataframe
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                qmatoms_str = str(prep.qm_atoms)

            if file_name:
                mimicpy.utils.file_handler.write(qmatoms_str, file_name)
                print("Wrote list of QM atoms to {}".format(file_name))
            else:
                print(qmatoms_str)

    if args.fix:
        top = fixtop(args)
        mpt = mimicpy.Mpt(top.molecules, top.topol_dict)
    else:
        mpt = get_nsa_mpt(args)

    print('')
    loader = Loader('**Reading coordinates**')

    try:
        selector = mimicpy.DefaultSelector(mpt, args.coords, buffer=args.bufc)
        prep = mimicpy.Preparation(selector)
    except FileNotFoundError as e:
        print('\n\nError: Cannot find file {}! Exiting..\n'.format(e.filename))
        loader.close(halt=True)
        sys.exit(1)
    except (mimicpy.utils.errors.ParserError, mimicpy.utils.errors.MiMiCPyError) as e:
        print(e)
        loader.close(halt=True)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Reading halted\n")
        loader.close(halt=True)
        sys.exit(1)

    loader.close()

    readline.parse_and_bind('set editing-mode vi') # handle command history

    dispatch = {'add':prep.add,
                'add-link': lambda selection: prep.add(selection, True),
                'delete':prep.delete,
                'clear': prep.clear,
                'view':view,
                'help':selection_help}

    def check_user_input(user_input):
        user_input = user_input.split()
        try:
            command = user_input[0].lower()
        except IndexError: # handle empty commands
            return False

        selection = ' '.join(user_input[1:])
        try:
            dispatch[command](selection)
        except mimicpy.utils.errors.SelectionError as e:  # Selection errors
            print(e)
        except TypeError:  # include functions without argument
            dispatch[command]()
        except KeyError: # invalid commands
            print("{} is an invalid command! Please try again. Type 'help' for more information.".format(command))

    def do_prep():
        try:
            if not prep.qm_atoms.empty:
                if args.link:
                    prep.find_link_atoms()

                prep.get_mimic_input(args.inp, args.ndx, args.out,
                                     args.pad, args.abs, args.qma,
                                     args.path, args.q, args.pp)

                if args.mdp:
                    print("Checking that {} is consistent with a MiMiC run".format(args.mdp))
                    prepmm(argparse.Namespace(mdp=args.mdp, qma=args.qma, out=None))

                    print("\nGenerating GROMACS TPR file using {} grompp\n".format(args.gmx))
                    import subprocess
                    subprocess.Popen("{} grompp -f {} -c {} -p {} -n {} -o {} -quiet".format(args.gmx, args.mdp,
                                                                                        args.coords, args.top,
                                                                                        args.ndx, args.tpr),
                                                                                        stdout=subprocess.PIPE, shell=True).stdout.read()
                else:
                    print("MDP file not passed! Skipping generation of GROMACS TPR file")
        except (mimicpy.utils.errors.SelectionError, mimicpy.utils.errors.MiMiCPyError) as error:
            print(error)
            sys.exit()

    if args.sele:
        print("Reading selection from {}".format(args.sele))

        if not isfile(args.sele):
            print("Error: Cannot find file {}! Exiting..\n".format(args.sele))
            sys.exit(1)
        else:
            sele_txt =  mimicpy.utils.file_handler.read(args.sele)

        for line in sele_txt.splitlines():
            if check_user_input(line) == False:
                continue

        do_prep()
    else:
        print("\nPlease enter selection below. For more information type 'help'")

    while not args.sele:
        try:
            user_input = input('> ')
        except KeyboardInterrupt:
            print("Exiting without writing\n")
            sys.exit()

        if user_input.strip() in ['quit', 'q']:
            do_prep()
            break

        if check_user_input(user_input) == False:
            continue

def get_nsa_mpt(args, only_nsa=False):
    nsa_dct = {}
    if args.nsa:
        if args.top.split('.')[-1] == 'mpt':
            print("Non-standard atomtype file ignored as .mpt file was passed")
        else:
            print("\n**Reading non-standard atomtypes file**\n")

            if not isfile(args.nsa):
                print("Error: Cannot find file {}! Exiting..\n".format(args.nsa))
                sys.exit(1)
            else:
                nsa_txt =  mimicpy.utils.file_handler.read(args.nsa)
                for i, line in enumerate(nsa_txt.splitlines()):
                    splt = line.split()
                    if len(splt) < 2:
                        print("Line {} in {} is not in 2-column format!\n".format(i+1, args.nsa))
                        sys.exit(1)
                    elif len(splt) > 2:
                        print("Line {} in {} has more than 2-columns. \
                              Using first two values only.\n".format(i+1, args.nsa))

                    nsa_dct[splt[0]] = splt[1]

    if nsa_dct != {}:
        print("The following atomypes were read from {}:\n".format(args.nsa))
        mimicpy.utils.strings.print_dict(nsa_dct, "Atom Type", "Element", print)

    if only_nsa:
        return nsa_dct

    print("\n**Reading topology**\n")
    try:
        return mimicpy.Mpt.from_file(args.top, mode='w', nonstandard_atomtypes=nsa_dct,
                                buffer=args.buf, gmxdata=args.ff, guess_elements=args.guess)
    except FileNotFoundError as e:
        print('\n\nError: Cannot find file {}! Exiting..\n'.format(e.filename))
        sys.exit(1)
    except mimicpy.utils.errors.ParserError as e:
        print(e)
        sys.exit(1)

def getmpt(args):
    get_nsa_mpt(args).write(args.mpt)

def cpmd2coords(args):
    mpt = get_nsa_mpt(args)
    try:
        cpmd = mimicpy.CpmdScript.from_file(args.inp)
    except mimicpy.utils.errors.ParserError as e:
        print(e)
        sys.exit(1)
    except FileNotFoundError as e:
        print('\n\nError: Cannot find file {}! Exiting..\n'.format(e.filename))
        sys.exit(1)

    print('')
    loader = Loader('**Writing coordinates**')

    try:
        cpmd.to_coords(mpt, args.coords, title='Coordinates from {}'.format(args.inp))
    except mimicpy.utils.errors.MiMiCPyError as e:
        print(e)
        loader.close(halt=True)
        sys.exit(1)

    loader.close()

def fixtop(args):
    nsa_dct = get_nsa_mpt(args, True)
    print("\n**Reading topology**\n")
    try:
        top = mimicpy.Top(args.top, mode='w', buffer=args.buf, nonstandard_atomtypes=nsa_dct,
                        gmxdata=args.ff, guess_elements=args.guess)
    except FileNotFoundError as e:
        print('\n\nError: Cannot find file {}! Exiting..\n'.format(e.filename))
        sys.exit(1)
    except mimicpy.utils.errors.ParserError as e:
        print(e)
        sys.exit(1)
    print("\n**Writing fixed [ atomtypes ] section**\n")

    try:
        top.write_atomtypes(args.fix, args.cls)
    except FileNotFoundError as e:
        print('\n\nError: Cannot find file {}! Exiting..\n'.format(e.filename))
        sys.exit(1)
    except FileExistsError as e:
        print(e)
        sys.exit(1)
    return top

def prepmm(args):
    try:
        mimicpy.Preparation.get_gmx_input(inp=args.mdp, qmatoms=args.qma, out=args.out)
    except FileNotFoundError as e:
        print('\n\nError: Cannot find file {}! Exiting..\n'.format(e.filename))
        sys.exit(1)
    except mimicpy.utils.errors.ScriptError as e:
        print(e)
        sys.exit(1)

def main():
    print('\n \t                ***** MiMiCPy *****                  ')
    print('\n \t For more information type mimicpy [subcommand] --help \n')

    parser = argparse.ArgumentParser(prog='mimicpy')
    subparsers = parser.add_subparsers(title='valid subcommands',
                                       metavar='')  # Turns off list of subcommands

    #####
    parser_prepqm = subparsers.add_parser('prepqm',
                                          help='create CPMD/MiMiC input and GROMACS index files')
    prepqm_input = parser_prepqm.add_argument_group('options to specify input')
    prepqm_input.add_argument('-top',
                              required=True,
                              help='topology file',
                              metavar='[.top/.mpt]')
    prepqm_input.add_argument('-coords',
                              required=True,
                              help='coordinate file',
                              metavar='[.gro/.pdb]')
    prepqm_input.add_argument('-mdp',
                              required=False,
                              help='MDP script to generate GROMACS TPR file',
                              metavar='[.mdp]')
    prepqm_output = parser_prepqm.add_argument_group('options to specify output')
    prepqm_output.add_argument('-out',
                               default='cpmd.inp',
                               help='CPMD script for MiMiC run',
                               metavar='[.inp] (cpmd.inp)')
    prepqm_output.add_argument('-ndx',
                               default='index.ndx',
                               help='Gromacs index file',
                               metavar='[.ndx] (index.ndx)')
    prepqm_output.add_argument('-fix',
                               required=False,
                               help='optional argument to specify fixed .itp file',
                               metavar='[.itp]')
    prepqm_output.add_argument('-tpr',
                              required=False,
                              default='mimic.tpr',
                              help='Output GROMACS TPR filename',
                              metavar='[.tpr] (mimic.tpr)')
    prepqm_others = parser_prepqm.add_argument_group('other options')
    prepqm_others.add_argument('-guess',
                              required=False,
                              default=True,
                              type=__str2bool,
                              help='toggle guessing atomic elements',
                              metavar='(True)')
    prepqm_others.add_argument('-sele',
                              required=False,
                              help='file containing selection',
                              metavar='[.txt/.dat]')
    prepqm_others.add_argument('-pp',
                               required=False,
                               help='file containing pseudopotential information',
                               metavar='[.dat]')
    prepqm_others.add_argument('-link',
                              required=False,
                              default=False,
                              type=__str2bool,
                              help='toggle guessing link atoms',
                              metavar='(False)')
    prepqm_others.add_argument('-nsa',
                              required=False,
                              help='file containing non-standard atomtypes in 2-column format',
                              metavar='[.txt/.dat]')
    prepqm_others.add_argument('-ff',
                              required=False,
                              help='path to force field data directory',
                              metavar='')
    prepqm_others.add_argument('-inp',
                              required=False,
                              help='CPMD template input script',
                              metavar='[.inp]')
    prepqm_others.add_argument('-gmx',
                              required=False,
                              default='gmx',
                              help='GROMACS executable to automatically generate TPR file',
                              metavar='(gmx)')
    prepqm_others.add_argument('-pad',
                              required=False,
                              type=__str2float,
                              default=0.0,
                              help='extra distance between qm atoms and wall in nm',
                              metavar='(0)')
    prepqm_others.add_argument('-abs',
                              required=False,
                              default=False,
                              type=__str2bool,
                              help='return QM cell size as absolute',
                              metavar='(False)')
    prepqm_others.add_argument('-qma',
                              required=False,
                              default='QMatoms',
                              help='name of QM atoms group in index file',
                              metavar='(QMatoms)')
    prepqm_others.add_argument('-path',
                              required=False,
                              help='path in the MIMIC section, overrides template',
                              metavar='')
    prepqm_others.add_argument('-q',
                              required=False,
                              type=__str2float,
                              help='charge of QM region, overrides default charge calculation',
                              metavar='')
    prepqm_others.add_argument('-buf',
                              required=False,
                              default=1000,
                              type=__str2int,
                              help='buffer size for reading input topology',
                              metavar='(1000)')
    prepqm_others.add_argument('-bufc',
                              required=False,
                              default=1000,
                              type=__str2int,
                              help='buffer size for reading input coordinates',
                              metavar='(1000)')
    prepqm_others.add_argument('-cls',
                              required=False,
                              help='clear [ atomtypes ] sections from list of files if -fix option is enabled',
                              nargs='*',
                              metavar='.itp')
    parser_prepqm.set_defaults(func=prepqm)
    ##
    #####
    parser_prepmm = subparsers.add_parser('prepmm',
                                          help='create/fix GROMACS MDP script for MiMiC run')
    prepmm_input = parser_prepmm.add_argument_group('options to specify input files')
    prepmm_input.add_argument('-mdp',
                              required=False,
                              help='MDP template script',
                              metavar='[.mdp]')
    prepmm_input.add_argument('-qma',
                              required=False,
                              help='name of QM atoms group',
                              metavar='QMatoms')
    prepmm_output = parser_prepmm.add_argument_group('options to specify output')
    prepmm_output.add_argument('-out',
                               default='mimic.mdp',
                               help='fixed MDP script for MiMiC run',
                               metavar='[.mdp] (mimic.mdp)')
    parser_prepmm.set_defaults(func=prepmm)
    ##
    #####
    parser_cpmd2coords = subparsers.add_parser('cpmd2coords',
                                          help='convert CPMD/MiMiC input to coordinates')
    cpmd2coords_input = parser_cpmd2coords.add_argument_group('options to specify input')
    cpmd2coords_input.add_argument('-top',
                              required=True,
                              help='topology file',
                              metavar='[.top/.mpt]')
    cpmd2coords_input.add_argument('-inp',
                              required=True,
                              help='CPMD input script with MIMIC/ATOMS sections',
                              metavar='[.inp]')
    cpmd2coords_output = parser_cpmd2coords.add_argument_group('options to specify output')
    cpmd2coords_output.add_argument('-coords',
                               default='mimic.gro',
                               help='coordinate file from CPMD/MIMIC script',
                               metavar='[.gro/.pdb] (mimic.gro)')
    cpmd2coords_others = parser_cpmd2coords.add_argument_group('other options')
    cpmd2coords_others.add_argument('-guess',
                              required=False,
                              type=__str2bool,
                              help='toggle guessing atomic elements',
                              metavar='(True)')
    cpmd2coords_others.add_argument('-nsa',
                              required=False,
                              help='file containing list of non-standard atomtypes',
                              metavar='[.txt/.dat]')
    cpmd2coords_others.add_argument('-ff',
                              required=False,
                              help='path to force field data directory',
                              metavar='')
    cpmd2coords_others.add_argument('-buf',
                              required=False,
                              default=1000,
                              type=__str2int,
                              help='buffer size for reading input topology',
                              metavar='(1000)')
    parser_cpmd2coords.set_defaults(func=cpmd2coords)
    ##
    #####
    parser_fixtop = subparsers.add_parser('fixtop',
                                          help='fix [ atomtypes ] section of GROMACS topology')
    fixtop_input = parser_fixtop.add_argument_group('options to specify input files')
    fixtop_input.add_argument('-top',
                              required=True,
                              help='GROMACS topology file',
                              metavar='[.top]')
    fixtop_output = parser_fixtop.add_argument_group('options to specify output files')
    fixtop_output.add_argument('-fix',
                               default='atomtypes.itp',
                               help='fixed .itp file',
                               metavar='[.itp] (atomtypes.itp)')
    fixtop_others = parser_fixtop.add_argument_group('other options')
    fixtop_others.add_argument('-guess',
                              required=False,
                              default=True,
                              help='toggle guessing atomic elements',
                              metavar='(True)')
    fixtop_others.add_argument('-nsa',
                              required=False,
                              help='file containing list of non-standard atomtypes',
                              metavar='[.txt/.dat]')
    fixtop_others.add_argument('-ff',
                              required=False,
                              help='path to force field data directory',
                              metavar='')
    fixtop_others.add_argument('-cls',
                              required=False,
                              help='clear atomtypes sections from list of files',
                              nargs='*',
                              metavar='.itp')
    fixtop_others.add_argument('-buf',
                              required=False,
                              default=1000,
                              type=__str2int,
                              help='buffer size for reading input topology',
                              metavar='(1000)')
    parser_fixtop.set_defaults(func=fixtop)
    ##
    #####
    parser_getmpt = subparsers.add_parser('getmpt',
                                          help='create MiMiCPy topology from GROMACS topology')
    getmpt_input = parser_getmpt.add_argument_group('options to specify input')
    getmpt_input.add_argument('-top',
                              required=True,
                              help='GROMACS topology file',
                              metavar='[.top]')
    getmpt_output = parser_getmpt.add_argument_group('options to specify output')
    getmpt_output.add_argument('-mpt',
                               default='topol.mpt',
                               help='MiMiCPy topology file',
                               metavar='[.mpt] (topol.mpt)')
    getmpt_others = parser_getmpt.add_argument_group('other options')
    getmpt_others.add_argument('-guess',
                              required=False,
                              default=True,
                              type=__str2bool,
                              help='toggle guessing atomic elements',
                              metavar='(True)')
    getmpt_others.add_argument('-nsa',
                              required=False,
                              help='list of non-standard atomtypes',
                              metavar='[.txt/.dat]')
    getmpt_others.add_argument('-ff',
                              required=False,
                              help='path to force field data directory',
                              metavar='')
    getmpt_others.add_argument('-buf',
                              required=False,
                              default=1000,
                              type=__str2int,
                              help='buffer size for reading input topology',
                              metavar='(1000)')
    parser_getmpt.set_defaults(func=getmpt)
    ##
    args = parser.parse_args()
    if vars(args) == {}:
        sys.exit()
    subcommand = args.func.__name__
    print('=====> Running {} <=====\n'.format(subcommand))
    args.func(args)
    print('\n=====> Done <=====\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
