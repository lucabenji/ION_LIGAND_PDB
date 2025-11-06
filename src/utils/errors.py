class CommandError(Exception):
    """
    Custom error raised when something is wrong with a command.
    """
    def __init__(self, command, message):
        self.command = command
        self.message = message
        super().__init__(f'{command}: {message}')

class InputFileError(Exception):
    """
    Custom error raised when input file is not found
    """
    def __init__(self, file) -> None:
        self.file = file
        self.message = '{}: input file not found!'.format(file)
        super().__init__(self.message)

class HelpRequest(CommandError):
    """
    Custom exception raised when help is request for a command.
    """
    def __init__(self, command):
        self.command = command
        message = 'help request!'
        super().__init__(command, message)

class LigandFileError(Exception):
    """
    Custom error when loading ligand files.
    """
    def __init__(self, filename, message) -> None:
        self.filename = filename
        self.message = message
        super().__init__(filename, message)

class ParserError(Exception):
    """
    Custom error raised when something is wrong with command parsing.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class PlacingError(Exception):
    """
    Custom error when placing a molecule.
    """
    def __init__(self, message) :
        self.message = message
        super().__init__(message)