class ParserError(Exception):
    """Custom exception for parser errors."""
    pass

class CommandError(Exception):
    def __init__(self, command, message):
        self.command = command
        self.message = message
        super().__init__(f'{command}: {message}')