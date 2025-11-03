"""
Execute commands from ION_LIGAND_PDB program.
"""
from typing import List
import sys

from src.parser import command_parser, command_subparsers
from src.utils import CommandError, HelpRequest, ParserError


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
    CommandError
        Raised if the request command is not available
    HelpRequest
        Raised if there is an help request
    """
    cm = command[0]

    # check if command is available
    if cm not in list_of_commands:
        raise CommandError(cm, 'command not found!')
    # check if help is requested
    elif ('-h' in command) or ('--help' in command):
        raise HelpRequest(cm)

def execute_command(command: List[str], interactive_mode = False):
    """
    Parse and execute a command line.

    Parameters
    ----------
    command : List[str]
        Command line to be executed
    """
    # execute command unless help is request or command is not available
    execution = True
    try:
        check_command(command)
    # help request
    except HelpRequest as e:
        command_subparsers.choices[e.command].print_help()
        execution = False
    #command not available
    except CommandError as e:
        print('{} not in available commands.'.format(e.command))
        print(f'Available commands are: {str_cm}')
        execution = False

    if execution:
        try:
            args = command_parser.parse_args(command)
            args.func(args)
        # error when parsing 
        except ParserError as e:
            print('Error: {}'.format(e.message))
            command_subparsers.choices[command[0]].print_usage()
            # quit if reading mode is on
            if interactive_mode == False:
                print('Quitting due to error(s)!')
                sys.exit()
        # error when command is executed
        except CommandError as e:
            print('{}: Error! {}'.format(e.command, e.message))
            # quit if reading mode is on
            if interactive_mode == False:
                print('Quitting due to error(s)!')
                sys.exit()