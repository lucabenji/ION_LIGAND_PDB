"""
System module
"""
import numpy as np
import typing as tp

from src.utils import random_place_molecules, write_pdb_line, evaluate_concentration
from src import Residue
from src.utils import PlacingError

class System:
    """
    System
    ------
    Generate a molecuar system where to add Residues.
    
    Attributes
    ----------
    residues : List[Residues] 
        The list of added Residues
    box : np.ndarray
        A numpy array of shape (3,) that contain the system box dimensions in Ang
    volume : float
        The volume of the system in cubic Ang
    n_atoms: int
        The total number of atoms in the system  
    n_res : int
        The number of Residues present in the system
    """

    def __init__(self, res_list: tp.List[Residue]=[]):

        """
        Initialize a System istance.

        Parameters
        ----------
        res_list : List[Residues], optional 
            The list of Residues, by default is []
        """
        
        self.residues = res_list
        
        self.__box = np.array([40.0, 40.0, 40.0])

    @property
    def box(self) -> np.ndarray:
        """
        A numpy array of shape (3,) that contain the system box dimensions in Ang.

        Returns
        -------
        np.ndarray
            A numpy array of shape (3,) that contain the system box dimensions in Ang
        """
        return self.__box
    
    @box.setter
    def box(self, box_dim: np.ndarray):
        """
        Set the system box dimensions in Ang.

        Parameters
        ----------
        box_dim : np.ndarray
            A numpy array of shape (3, ) with the system box dimensions in Ang
        """
        self.__box = box_dim

    @property
    def volume(self) -> float:
        """
        The volume of the system in cubic Ang.

        Returns
        -------
        float
            The volume of the system in cubic Ang
        """
        return np.prod(self.__box, dtype=float)


    @property
    def system_coords(self) -> tp.List[np.ndarray]:
        """
        List of all the atomic coordinates of the system. Each list element correspond to the atomic coordinates of a specific Residue.

        Returns
        -------
        tp.List[np.ndarray]
            List of all the atomic coordinates of the system
        """
        
        coords = []
        for res in self.residues:
            coords.append(res.coords)

        return coords
    
    @property
    def n_atoms(self) -> int:
        """
        The total number of atoms in the system.

        Returns
        -------
        int
            The total number of atoms in the system
        """

        n = 0
        for res in self.residues:
            n += res.n_atoms
        
        return n

    @property
    def n_res(self) -> int:
        """
        The total number of Residues in the system.

        Returns
        -------
        int
            The total number of Residues in the system
        """
        return len(self.residues)
        

    def add_residue(self, res: Residue, cutoff=4.0, n=1):
        """
        Add Residue(s) to the system.

        Parameters
        ----------
        res : Residue
            The Residue to be added.
        cutoff : float, optional
            The minimum distance that the new Residue(s) must have from the other atoms of the system, by default 4.0
        n : int, optional
            The number of Residue(s) to be added, by default 1
        """
        
        # center the coordinate of the new residue
        res.centering()

        # generate new residue coordinates
        try:
            new_coords = random_place_molecules(res.coords, self.box, cutoff, n, self.system_coords)
        except PlacingError as e:
            msg = 'Error when placing {} residue(s) {} with minimum distance {:.2f} Ang. {}'.format(n, res.resname, cutoff, e.message)
            raise PlacingError(msg)

        # add new residues
        for i in range(self.n_res, self.n_res + n):
            new_res = res.copy()
            new_res.coords = new_coords[i]
            self.residues.append(new_res)
        
        # enumerate new residues and atoms
        self.enumerate_residues()

    def enumerate_residues(self):
        """
        Enumerate Residues and atoms of the system. Enumeration follows the order of System.residues list.
        """

        count_res = 0
        count_atm = 1

        for res in self.residues:
    
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
        Get the number of a specific Residue in the system based on its Residue name.

        Parameters
        ----------
        resname : str
            The Residue name to count.

        Returns
        -------
        int
            The number of the specified Residue in the system.
        """

        count = 0
        for res in self.residues:
            if res.resname == resname:
                count += 1
        
        return count
    
    def get_res_concentration(self, resname: str) -> float:
        """
        Get the molar concentration of a specific Residue in the system based on its Residue name.

        Parameters
        ----------
        resname : str
            The Residue name of interest.

        Returns
        -------
        float
            The molat concentration of the specified Residue in the system.
        """

        n_res = self.get_number_of_res(resname)

        conc = evaluate_concentration(n_res, self.volume)

        return conc
    
    def remove_residue(self, resname: str):
        """
        Remove specific Residue(s) from the system based on the Residue name.

        Parameters
        ----------
        resname : str
            The Residue name to be removed. 
        """  
        self.residues = [res for res in self.residues if res.resname != resname]

        self.enumerate_residues()