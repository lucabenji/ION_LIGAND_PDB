"""
Function for fancy printing at the start and end of the program.
"""

start_print = r"""
 _____            _     _                       ___________________  
|_   _|          | |   (_)                     | | ___ \  _  \ ___ \ 
  | |  ___  _ __ | |    _  __ _  __ _ _ __   __| | |_/ / | | | |_/ /    
  | | / _ \| '_ \| |   | |/ _` |/ _` | '_ \ / _` |  __/| | | | ___ \     
 _| || (_) | | | | |___| | (_| | (_| | | | | (_| | |   | |/ /| |_/ /   
 \___/\___/|_| |_\_____/_|\__, |\__,_|_| |_|\__,_\_|   |___/ \____/  
                           __/ |                                    
                          |___/                                      

"""                                 

end_print = """
    ╭──────────────────────────────────────────────╮
    │                                              |
    │       Thanks for using ION_LIGAND_PDB.       │
    │                                              │
    │                               Goodbye!       │
    │                                              │
    ╰──────────────────────────────────────────────╯
"""

def start(interactive_mode: bool):
    """
    Fancy print when the program start.

    Parameters
    ----------
    interactive_mode : bool
        If true, print additional lines for the interactive mode.
    """

    print(start_print)

    print("\nWelcome to the Ion Ligand PDB Generator!")
    print("It's time to create your metal ion-ligand PDB file, lets go!")

    if interactive_mode == True:
        print("Type 'quit' to exit.")

def end():
    """
    Fancy print when quitting the program
    """

    print(end_print)