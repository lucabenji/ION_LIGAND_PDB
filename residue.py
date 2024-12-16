"""Residue"""

import numpy as np

from functions import center_coords

class Residue:

    def __init__(self, atom_list=[], coords=[], res_name=None):
        
        self.atoms = atom_list
        self.coords = coords
        self.name = res_name
        self.n_atoms = len(self.atoms)
    
    def copy(self):
        return Residue(self.atoms, self.coords, self.name)
    
    @classmethod
    def read_from_pdb(cls, filename, res_name):

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
    
        
        return cls(atoms, np.array(coordinates), res_name)
    
    def centering(self):
        
        self.coords = center_coords(self.coords)