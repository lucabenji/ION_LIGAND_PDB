"""
Function for fancy printing at the start of the program.
"""

line1 = ' _____            _     _                       ___________________  '
line2 = '|_   _|          | |   (_)                     | | ___ \\  _  \\ ___ \\ '
line3 = '  | |  ___  _ __ | |    _  __ _  __ _ _ __   __| | |_/ / | | | |_/ /    '
line4 = "  | | / _ \\| '_ \\| |   | |/ _` |/ _` | '_ \\ / _` |  __/| | | | ___ \\     " 
line5 = " _| || (_) | | | | |___| | (_| | (_| | | | | (_| | |   | |/ /| |_/ /    "
line6 = " \\___/\\___/|_| |_\\_____/_|\\__, |\\__,_|_| |_|\\__,_\\_|   |___/ \\____/  "
line7 = "                           __/ |                                    "
line8 = "                          |___/                                     "

def start(interactive_mode: bool):
    """
    Fancy print when the program start.

    Parameters
    ----------
    interactive_mode : bool
        If true, print additional lines for the interactive mode.
    """

    print(line1)
    print(line2)
    print(line3)
    print(line4)
    print(line5)
    print(line6)
    print(line7)
    print(line8)

    print("\nWelcome to the Ion Ligand PDB Generator!")
    print("It's time to create your metal ion-ligand PDB file, lets go!")

    if interactive_mode == True:
        print("Type 'quit' to exit.")