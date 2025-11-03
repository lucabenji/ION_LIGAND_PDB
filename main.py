"""
Main execution file for ION LIGAND PDB .
"""
import sys

# loading parser option
from src.parser import interactive_mode_status, input_file, InputReader
from src.execution import execute_command
from src.utils.errors import InputFileError

# fancy start printing
from src.utils import start

# check operation mode
interactive_mode = interactive_mode_status

def main():
    """
    Main execution function.
    """

    # fancy print
    start(interactive_mode=interactive_mode_status)
    
    # interactive mode
    while interactive_mode == True:
        command_line = input("\n> ")
        execute_command(command_line.split(), interactive_mode=interactive_mode)


    # reading command from input file
    try:
        reader = InputReader(input_file=input_file)
        reader.read_and_execute()
    except InputFileError as e:
        print(e.message)
        sys.exit()

if __name__ == "__main__":
    main()