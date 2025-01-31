# class System
import numpy as np
import typing as tp

from src.utils.functions import random_place_molecules, write_pdb_line, evaluate_concentration
from src.residue import Residue

class System:
    """
    System
    ------
    Generate a molecuar system where to add Residues.
    
    Attributes:
    ----------
        residues (List[Residues]) 
            list of added Residues (default is an empty list)

        box (np.ndarray)
            array of shape (3,) that contain the system box dimensions (default is np.ndarray([40.0, 40.0, 40.0]))

        volume (float) 
            volume of the system

        n_atoms (int)
            number of atoms present in the system
        
        n_res (int)
            number of Residues present in the system
    """

    def __init__(self, res_list: tp.List[Residue]=[], box=np.array([40.0, 40.0, 40.0])):
        """
        Initialize a System istance.

        Args:
        ----
            res_list (List[Residues]) 
                list of Residues (default is an empy list)
            
            box (np.ndarray)
                array of shape (3, ) containing the system box dimensions (default is np.ndarray([40.0, 40.0, 40.0]))
        """
        
        self.residues = res_list
        self.__box = box

    @property
    def box(self):
        """
        Get system box dimensions.

        Returns:
        -------
            box (nd.array):
                array of shape (3, ) containing the system box dimensions (default is np.ndarray([40.0, 40.0, 40.0]))
        """
        return self.__box
    
    @box.setter
    def box(self, box_dim: np.ndarray):
        """
        Set system box dimensions.

        Args:
        ----
            box_dim (np.ndarray)
                array of shape (3, ) containing the system box dimensions
        """
        self.__box = box_dim

    @property
    def volume(self) -> float:
        """
        Get system box volume.

        Returns:
        -------
            (float)
                System box volume.
        """
        return np.prod(self.__box)
    
    #@property
    #def system_atoms(self):
        
    #    atoms = []
    #    for res in self.residues:
    #        atoms += res.atoms
    #    return atoms

    @property
    def system_coords(self) -> tp.List[np.ndarray]:
        """
        Get system stomic coordinates.
        """
        
        coords = []
        for res in self.residues:
            coords.append(res.coords)

        return coords
    
    @property
    def n_atoms(self) -> int:
        """
        Get system total number of atoms.
        """

        n = 0
        for res in self.residues:
            n += res.n_atoms
        
        return n

    @property
    def n_res(self) -> int:
        """
        Get system total number of Residues.
        """
        return len(self.residues)
        

    def add_residue(self, res: Residue, cutoff=4.0, n=1):
        """
        Add a specified number of Residues to the system.

        Args:
        ----
            res (Residue)
                Residue to be added
            
            cutoff (float)
                minimum distance in Ang where to place the new residue(s) (default is 4.0)

            n (int)
                number of Residues to add (default is 1)
        """
        
        # center the coordinate of the new residue
        res.centering()

        # generate new residue coordinates
        new_coords = random_place_molecules(res.coords, self.box, cutoff, n, self.system_coords)

        # add new residues
        for i in range(self.n_res, self.n_res + n):
            new_res = res.copy()
            new_res.coords = new_coords[i]
            self.residues.append(new_res)
        
        # enumerate new residues and atoms
        self.enumerate_residues()

    def enumerate_residues(self):
        """
        Enumerate Residues and atoms of the system.
        """

        count_res = 1
        count_atm = 1

        for res in self.residues:
            res
            res.res_num = count_res
            res.atom_id = np.arange(count_atm, count_atm + res.n_atoms)

            count_res += 1
            count_atm += res.n_atoms

    def generate_pdb(self):
        """
        Generate a PDB file of the system.
        """

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
        """
        Get the number of a specific Residue in the system based on its residue name.

        Args:
        ----
            resname (str)
                residue name of the Residue of interest

        Returns:
        -------
            (int)
                number of specified Residue in the system
        """
        count = 0
        for res in self.residues:
            if res.resname == resname:
                count += 1
        
        return count
    
    def get_res_concentration(self, resname: str) -> float:
        """
        Get the molar concentration of a specific Residue in the system based on its residue name.

        Args:
        ----
            resname (str)
                residue name of the Residue of interest

        Returns:
        -------
            (float)
                molar concentration of specified Residue in the system
        """
        n_res = self.get_number_of_res(resname)

        conc = evaluate_concentration(n_res, self.volume)

        return conc
    
    def remove_residue(self, resname: str):
        """
        Remove a specific Residue from the system based on its residue name.

        Args:
        ----
            resname (str)
                residue name of the Residue to be removed
        """


        for res in self.residues:
            if res.resname == resname:
                self.residues.remove(res)

        self.enumerate_residues()