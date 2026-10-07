"""
Execution modules

It contains functions that check, parse, and execute commands for ION_LIGAND_PDB program.
"""
from typing import List
import sys

from src.parser import command_parser, command_subparsers
from src.utils import ExecutionError, HelpRequest, ParserError


# list of all commands
list_of_commands = command_subparsers.choices.keys()
str_cm = ', '.join(cm for cm in list_of_commands)


def check_command(command: List[str]):
    """
    Check if a command is available and print help message if request.

    Parameters
    ----------
    command : List[str]
        Command line.

    Raises
    ------
    ExecutionError
        Raised if the request command is not available
    HelpRequest
        Raised if there is an help request
    """
    command_name = command[0]

    # check if command is available
    if command_name not in list_of_commands:
        msg = f'{command_name}: command not found!'
        raise ExecutionError(msg)
    # check if help is requested
    elif ('-h' in command) or ('--help' in command):
        raise HelpRequest(command_name)

def execute_command(command: List[str], interactive_mode = False):
    """
    Parse and execute a command line.

    Parameters
    ----------
    command : List[str]
        Command line to be executed
    """
    # execute command unless help is requested or command is not available
    execution = True
    command_name = command[0]
    try:
        check_command(command)
    # help request
    except HelpRequest as e:
        command_subparsers.choices[command_name[0]].print_help()
        execution = False
    #command not available
    except ExecutionError as e:
        print(e.message)
        print(f'Available commands are: {str_cm}')
        execution = False

    if execution:
        try:
            args = command_parser.parse_args(command)
            args.func(args)
        # error when parsing 
        except ParserError as e:
            print('Error: {}'.format(e.message))
            command_subparsers.choices[command_name].print_usage()
            # quit if reading mode is on
            if interactive_mode == False:
                print('Quitting due to error(s)!')
                sys.exit()
        # error when command is executed
        except ExecutionError as e:
            print('{}: Error! {}'.format(command_name, e.message))
            # quit if reading mode is on
            if interactive_mode == False:
                print('Quitting due to error(s)!')
                sys.exit()