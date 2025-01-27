"""
Parser for the main program
"""

import os
import argparse

from commands import *

# Main parser
main_parser = argparse.ArgumentParser(description="Ion Ligand PDB generator by Luca B.", add_help=True)
main_parser.add_argument("-i", dest="input_file", help="Input file with command instructions.", default=None, type=str)
main_args = main_parser.parse_args()

# Main parse argument
input_file = main_args.input_file

# activate reading mode
if input_file is not None:
    print('Coming soon!')

# Command Parser
command_parser = argparse.ArgumentParser(prog="", add_help=False)
command_subparsers = command_parser.add_subparsers(dest="command", required=True) 

# add_ion parser
ion_parser = command_subparsers.add_parser('add_ion')
ion_parser.add_argument('ION', type=str, help='Name of the ion.')
ion_parser.add_argument('-n', dest='n', type=int, default=1, help='Number of ions (default=1)')
ion_parser.add_argument('-cutoff', dest='cutoff', type=float, default=4.0, help='Minimum distance for placing ions in Ang (default=4.0)')
ion_parser.set_defaults(func=add_ion)

# add_ligand parser
lig_parser = command_subparsers.add_parser('add_ligand')
lig_parser.add_argument('-f', dest='file_name', type=str, required=True, help='Ligand file name')
lig_parser.add_argument('-n', dest='n', type=int, default=1, help='Number of ligands (default=1)')
lig_parser.add_argument('-cutoff', dest='cutoff', type=float, default=4.0, help='Minimum distance for placing ligands in Ang (default=4.0)')
lig_parser.add_argument('RES', type=str, help='Ligand residue name (max. 3 characters)')
lig_parser.set_defaults(func=add_ligand)

# quit parser
quit_parser = command_subparsers.add_parser('quit')
quit_parser.set_defaults(func=quit)

# set_box parser
box_parser = command_subparsers.add_parser('set_box')
box_parser.add_argument('DIM', type=float, help='Box dimension in Ang.')
box_parser.set_defaults(func=set_box)

# set_volume parser
volume_parser = command_subparsers.add_parser('set_volume')
volume_parser.add_argument('VOL', type=float, help='Box volume in Ang^3.')
volume_parser.set_defaults(func=set_volume)

def execute_command(command):
    """
    """
    args = command_parser.parse_args(command.split())
    args.func(args)
