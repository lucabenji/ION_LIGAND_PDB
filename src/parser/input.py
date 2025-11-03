"""
Input module for input file parsing and execution of input file commands.


"""
import os

from src.execution import execute_command
from src.utils.errors import InputFileError

class InputReader:
    """
    InputReader
    -----------
    Read and execute commands from an input file.
    Lines starting with '#' will be ignored.

    Attributes
    ----------
    input_file : str
        Name or path of the input file.
    """

    def __init__(self, input_file: str):
        """
        InputReader initializer.

        Parameters
        ----------
        input_file : str
            Name or path of the input file.
        """

        if os.path.exists(input_file):
            self.input_file = input_file
        else:
            raise InputFileError(input_file)

    
    def read_and_execute(self):
        """
        Read and execute commands from the input file.
        """

        with open(self.input_file) as f:

            for line in f:
                
                # read lines, ignore comments that start with '#'
                command_line = line.split("#", 1)[0].strip()
                
                # execute commands
                if command_line:
                    print('\n>', command_line)                    
                    execute_command(command_line.split(), interactive_mode=False)