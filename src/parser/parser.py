"""
Parser module for the main program and available commands.

The main parser activates the interactive mode if no input files with command is provided.
"""

import argparse
import sys
from typing import List

from src.commands import *
from src.utils import CommandError, HelpRequest, ParserError

# Main parser
main_parser = argparse.ArgumentParser(description="Ion Ligand PDB generator by Luca B.", add_help=True)
main_parser.add_argument("-i", dest="input_file", help="Input file with command instructions.", default=None, type=str, metavar='input.in')
main_args = main_parser.parse_args()

# Main parse argument: input file
input_file = main_args.input_file

# activate reading mode or interactive mode
if input_file is not None:
    interactive_mode_status = False
else:
    interactive_mode_status = True

# Command Parser
class CommandParser(argparse.ArgumentParser):

    # custom error method for interactive vs reading mode
    def error(self, message: str):
        """
        Custom error method that raises ParsedError instad of quitting automatically.

        Parameters
        ----------
        message : str
            Error message

        Raises
        ------
        ParserError
            Custom error raised when an error is found douring parsing
        """

        raise ParserError(message)

# parser for commands
command_parser = CommandParser(prog="", add_help=False)
command_subparsers = command_parser.add_subparsers(dest="command", required=True) 

# add_ion parser
ion_parser = command_subparsers.add_parser('add_ion')
ion_parser.add_argument('ION', type=str, help='Name of the ion.')
ion_parser.add_argument('-cutoff', dest='cutoff', type=float, default=4.0, help='Minimum distance between ions and other molecules in Ang (default=4.0)')
# only one betwen number or concentration can be choosen
ion_number = ion_parser.add_mutually_exclusive_group()
ion_number.add_argument('-n', dest='N', type=int, nargs="?", default=1, help='Number of ions (default=1)')
ion_number.add_argument('-conc', dest='conc', type=float, help='Molar ion concentration.')
ion_parser.set_defaults(func=add_ion)

# add_ligand parser
lig_parser = command_subparsers.add_parser('add_ligand')
lig_parser.add_argument('RES', type=str, nargs="?", help='Ligand residue name (max. 3 characters)')
lig_parser.add_argument('-f', dest='file_name', type=str, required=True, help='Ligand file name')
lig_parser.add_argument('-cutoff', dest='cutoff', type=float, default=4.0, help='Minimum distance for placing ligands and other molecules in Ang (default=4.0)')
# only one between number or concentration can be choosen
lig_number = lig_parser.add_mutually_exclusive_group()
lig_number.add_argument('-n', dest='N', type=int, nargs="?", default=1, help='Number of ligands (default=1)')
lig_number.add_argument('-conc', dest='conc', type=float, help='Molar ligand concentration.')
lig_parser.set_defaults(func=add_ligand)

# generate_pdb parser
pdb_parser = command_subparsers.add_parser('generate_pdb')
#pdb_parser.add_argument('out_file', type=str, help='Name of the pdb file where the system will be saved.')
pdb_parser.set_defaults(func=generate_pdb)

# quit parser
quit_parser = command_subparsers.add_parser('quit')
quit_parser.set_defaults(func=quit)

# remove_ion parser
rm_ion_parser = command_subparsers.add_parser('remove_ion')
rm_ion_parser.add_argument('ION', type=str, help='Name of the ion to remove.')
rm_ion_parser.set_defaults(func=remove_ion)

# remove_lig parser
rm_lig_parser = command_subparsers.add_parser('remove_ligand')
rm_lig_parser.add_argument('LIG', type=str, help='Name of the ligand to remove.')
rm_lig_parser.set_defaults(func=remove_ligand)

# set_box parser
box_parser = command_subparsers.add_parser('set_box')
box_parser.add_argument('DIM', type=float, help='Box dimensions in Ang.')
box_parser.set_defaults(func=set_box)

# set_volume parser
volume_parser = command_subparsers.add_parser('set_volume')
volume_parser.add_argument('VOL', type=float, help='Box volume in Ang^3.')
volume_parser.set_defaults(func=set_volume)