# class System
import numpy as np
import typing as tp

from functions import random_place_molecules
from residue import Residue

class System:

    def __init__(self, res_list: tp.List[Residue]=[], box=np.array([40.0, 40.0, 40.0])):
        
        self.res_list = res_list
        self.box = box
        self.n_res = len(res_list)
        self.volume = np.prod(box)


    def add_residue(self, res: Residue, cutoff=4.0, n=1):
        
        sys_coords = self.get_system_coords()
        res.centering()
        new_coords = random_place_molecules(res.coords, self.box, cutoff, n, sys_coords)

        for i in range(self.n_res, self.n_res + n):
            new_res = res.copy()
            new_res.coords = new_coords[i]
            self.res_list.append(new_res)

        self.n_res += n
    
    def generate_pdb(self):
        
        format_line = (
        "ATOM  {atom_id:5d} {atom_name:>3s}{alternate_location} {residue_name:<3s} {chain_id}{residue_number:4d}    "
        "{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {element:>2}"
    )

        count_atm = 1
        for i in range(self.n_res):
            res = self.res_list[i]

            for j in range(res.n_atoms):
                pdb_line = format_line.format(atom_id=count_atm, 
                                              atom_name=res.atoms[j], 
                                              alternate_location=' ', 
                                              residue_name=res.name,
                                              chain_id = ' ',
                                              residue_number = i+1,
                                              x = res.coords[j, 0],
                                              y = res.coords[j, 1],
                                              z = res.coords[j, 2],
                                              element = ''
                                              ) 
                print(pdb_line)
                count_atm += 1
            print('TER')
        print('END')

    def get_system_coords(self):
        
        coords = []
        for res in self.res_list:
            coords.append(res.coords)

        return coords
    
    def set_box(self, box: np.ndarray):

        self.box = box
        self.volume = np.prod(box)