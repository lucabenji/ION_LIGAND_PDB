"""
Main execution file.
"""
#To do: reader inputfile option
#
from src.parser import interactive_mode_status, input_file, execute_command, InputReader

interactive_mode = interactive_mode_status

def main():
    print("Welcome to the Ion Ligand PDB Generator!")
    print("Type 'help' to see available commands. Type 'quit' to exit.")
    
    while interactive_mode == True:
        command_line = input("\n> ")
        execute_command(command_line.split())

    reader = InputReader(input_file=input_file)
    reader.read_and_execute()

if __name__ == "__main__":
    main()