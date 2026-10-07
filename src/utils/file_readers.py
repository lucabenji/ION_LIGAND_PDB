"""
This module contains all functions that read and extract information (atom names and coordinates) from molecular files.

Supported file formats: PBD (.pdb), MOL2 (.pdb), SDF (.sdf)
"""

import numpy as np
from typing import List, Tuple


def read_from_pdb(filename: str) -> Tuple[List, np.ndarray]:
    """
    Extract atom names and coordinates from a PDB file.

    The PDB file must respect the format:
    column 1-6: Record name "ATOM" or "HETATM"
    column 13-16: Atom name
    column 31-38: X coordinate in Ang
    column 39-46: Y coordinate in Ang
    column 47-54: Z coordinate in Ang 

    Parameters
    ----------
    filename : str
        Name of the PDB file.

    Returns
    -------
    Tuple[List, np.ndarray]
        List of atom names and array of coordinates.
    """

    atoms = []
    coordinates = []
    
    with open(filename, 'r') as file:
        for line in file:
                
            if line.startswith("ATOM") or line.startswith("HETATM"):
                
                atom_name = line[12:16].strip()  # Atom name
                x = float(line[30:38].strip())   # X coordinate
                y = float(line[38:46].strip())   # Y coordinate
                z = float(line[46:54].strip())   # Z coordinate 
                
                atoms.append(atom_name)
                coordinates.append([x, y, z])
    
        
    return atoms, np.array(coordinates)

def read_from_mol2(filename: str) ->  Tuple[List, np.ndarray]:
    """
    Extract atom names and coordinates from a MOL2 file.

    The MOL2 file must contain a @<TRIPOS>ATOM section with the format:
    "atom_id atom_name x y z atom_type residue_id residue_name charge"

    Parameters
    ----------
    filename : str
        MOL2 file name.

    Returns
    -------
    Tuple[List, np.ndarray]
        List of atom names and array of coordinates.
    """

    atoms = []
    coordinates = []

    with open(filename, "r") as file:
    
        in_atom_section = False  
        
        for line in file:
            if line.startswith("@<TRIPOS>ATOM"):
                # ATOM section
                in_atom_section = True
                continue
            elif line.startswith("@<TRIPOS>"):  
                break # End of ATOM section
            
            if in_atom_section:
                atom_line = line.split()
                if len(atom_line) >= 6:  

                    atom_name = atom_line[1] # Atom name
                    x = float(atom_line[2])  # X coordinate
                    y = float(atom_line[3])  # Y coordinate
                    z = float(atom_line[4])  # Z coordinate

                    atoms.append(atom_name)
                    coordinates.append([x, y, z])


    return atoms, np.array(coordinates)   

def read_from_sdf(filename: str) -> Tuple[List, np.ndarray]:
    """
    Extract atom names and coordinates from a SDF file.

    The 4th line of the SDF file must contain the number of atoms.
    Atom infotmations must be stored from the fith line in format:
    "x_coord y_coord z_coord atom_name ..."

    Parameters
    ----------
    filename : str
        SDF file name.

    Returns
    -------
    Tuple[List, np.ndarray]
        List of atom names and array of coordinates.
    """

    atoms = []  # List to store (atom_name, x, y, z)
    coordinates = []
    
    with open(filename, "r") as file:
        lines = file.readlines()

    # The 4th line contains the number of atoms
    counts_line = lines[3].split() # In an SDF file, the 4th line contains the number of atoms
    
    #if len(counts_line) < 2:
    #    msg = "Invalid SDF file format: missing atom and bond counts."
    #    raise LigandFileError(filename=filename, message=msg)

    # Number of atoms
    num_atoms = int(counts_line[0])
    # Atom block starts at the 5th line 
    atom_start = 4  

    # Read atom
    for i in range(num_atoms):
        atom_line = lines[atom_start + i].split()
        if len(atom_line) >= 4:
            x = float(atom_line[0])  # X coordinate
            y = float(atom_line[1])  # Y coordinate
            z = float(atom_line[2])  # Z coordinate
            atom_name = atom_line[3] # atom name
            
            atoms.append(atom_name)
            coordinates.append([x, y, z])

    return atoms, np.array(coordinates)


# dict with all the residue format file supported and the relative 
EXTRACT_RESIDUE = {
    ".pdb" : read_from_pdb,
    ".mol2": read_from_mol2,
    ".sdf": read_from_sdf
}