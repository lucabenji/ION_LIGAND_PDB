# class System
import numpy as np
import typing as tp

from functions import random_place_molecules, write_pdb_line, evaluate_concentration
from residue import Residue

class System:

    def __init__(self, res_list: tp.List[Residue]=[], box=np.array([40.0, 40.0, 40.0])):
        
        self.residues = res_list
        self.__box = box

    @property
    def box(self):
        return self.__box
    
    @box.setter
    def box(self, box_dim: np.ndarray):
        self.__box = box_dim

    @property
    def volume(self):
        return np.prod(self.__box)
    
    @property
    def system_atoms(self):
        
        atoms = []
        for res in self.residues:
            atoms += res.atoms
        return atoms

    @property
    def system_coords(self):
        
        coords = []
        for res in self.residues:
            coords.append(res.coords)

        return coords
    
    @property
    def n_atoms(self):

        n = 0
        for res in self.residues:
            n += res.n_atoms
        
        return n

    @property
    def n_res(self):
        return len(self.residues)
        

    def add_residue(self, res: Residue, cutoff=4.0, n=1):
        
        res.centering()

        new_coords = random_place_molecules(res.coords, self.box, cutoff, n, self.system_coords)

        for i in range(self.n_res, self.n_res + n):
            new_res = res.copy()
            new_res.coords = new_coords[i]
            new_res.res_num = i
            new_res.atom_id = res.atom_id + self.n_atoms
            self.residues.append(new_res)
    
    def generate_pdb(self):
   

        for res in self.residues:
            for i in range(res.n_atoms):
                pdb_line = write_pdb_line(atom_id=res.atom_id[i], 
                                              atom_name=res.atoms[i], 
                                              res_name=res.resname,
                                              res_number = res.res_num,
                                              coords = res.coords[i]
                                              ) 
                print(pdb_line)
            print('TER')
        print('END')

    def get_number_of_res(self, resname: str) -> int:
        
        count = 0
        for res in self.residues:
            if res.resname == resname:
                count += 1
        
        return count
    
    def get_res_concentration(self, resname: str) -> float:

        n_res = self.get_number_of_res(resname)

        conc = evaluate_concentration(n_res, self.volume)

        return conc