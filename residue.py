"""
Residue
"""

import typing as tp
import numpy as np

from functions import center_coords

class Residue:

    def __init__(self, atom_list: tp.List[str]=[], coords: tp.Union[list, np.ndarray]=[], res_name: tp.Optional[str]=None):
        
        self.atoms = atom_list
        self.coords = coords if type(coords) == np.ndarray else np.array(coords)
        self.resname = res_name

        self.__atom_id = np.arange(1, self.n_atoms + 1)
        self.__res_num = 1
    
    @property
    def n_atoms(self):
        return len(self.atoms)

    @property
    def atom_id(self):
        return self.__atom_id

    @atom_id.setter
    def atom_id(self, id_list: np.ndarray):
        self.__atom_id = id_list

    @property
    def res_num(self):
        return self.__res_num
    
    @res_num.setter
    def res_num(self, num):
        self.__res_num = num
    
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

    def copy(self):
        return Residue(self.atoms, self.coords, self.resname)