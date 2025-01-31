"""
Main execution file.
"""
#To do: reader inputfile option
#
from src.commands.parser import *

def main():
    print("Welcome to the Ion Ligand PDB Generator!")
    print("Type 'help' to see available commands. Type 'quit' to exit.")
    
    while True:
        command_line = input("> ")
        execute_command(command_line)

if __name__ == "__main__":
    main()