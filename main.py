"""
Main execution file.
"""
#To do: reader inputfile option
#
from parser import *

def main():
    print("Welcome to the Ion Ligand PDB Generator!")
    print("Type 'help' to see available commands. Type 'quit' to exit.")
    
    while True:
        command_line = input("> ").strip()
        execute_command(command_line)

if __name__ == "__main__":
    main()