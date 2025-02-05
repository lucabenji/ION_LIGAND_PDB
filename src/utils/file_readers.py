"""
This module contains all functions that read and extract information from molecular files.

Supported file formats (for now): PBD (.pdb), MOL2 (.pdb), SDF (.sdf)
"""

import numpy as np

def read_from_pdb(filename: str):

    atoms = []
    coordinates = []
    
    with open(filename, 'r') as file:
        for line in file:
                
            if line.startswith("ATOM") or line.startswith("HETATM"):
                
                atom_name = line[12:16].strip()  # Atom name (characters 13-16)
                x = float(line[30:38].strip())   # X coordinate (characters 31-38)
                y = float(line[38:46].strip())   # Y coordinate (characters 39-46)
                z = float(line[46:54].strip())   # Z coordinate (characters 47-54)
                
                atoms.append(atom_name)
                coordinates.append([x, y, z])
    
        
    return atoms, np.array(coordinates)

def read_from_mol2(filename: str):

    atoms = []
    coordinates = []

    with open(filename, "r") as file:
        in_atom_section = False  # Flag for ATOM section
        
        for line in file:
            if line.startswith("@<TRIPOS>ATOM"):
                in_atom_section = True
                continue
            elif line.startswith("@<TRIPOS>"):  # Stop at the end of atom section
                break
            
            if in_atom_section:
                atom_line = line.split()
                if len(atom_line) >= 6:  # Line must have enough data

                    atom_name = atom_line[1]
                    x = float(atom_line[2])
                    y = float(atom_line[3])
                    z = float(atom_line[4])

                    atoms.append(atom_name)
                    coordinates.append([x, y, z])


    return atoms, np.array(coordinates)   

def read_from_sdf(filename):

    atoms = []  # List to store (atom_name, x, y, z)
    coordinates = []
    
    with open(filename, "r") as file:
        lines = file.readlines()

    counts_line = lines[3].split() # In an SDF file, the 4th line contains the number of atoms
    
    if len(counts_line) < 2:
        raise ValueError("Invalid SDF file format: missing atom and bond counts.")

    num_atoms = int(counts_line[0])  # Number of atoms
    atom_start = 4  # Atom block starts at the 4th line

    # Read atom section
    for i in range(num_atoms):
        atom_line = lines[atom_start + i].split()
        if len(atom_line) >= 4: # line must have enough data
            x = float(atom_line[0])
            y = float(atom_line[1])
            z = float(atom_line[2])
            atom_name = atom_line[3]
            
            atoms.append(atom_name)
            coordinates.append([x, y, z])

    return atoms, np.array(coordinates)


# dict with all the residue format file supported and the relative 
EXTRACT_RESIDUE = {
    ".pdb" : read_from_pdb,
    ".mol2": read_from_mol2,
    ".sdf": read_from_sdf
}