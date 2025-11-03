"""
residue.py
==========


"""
import os

import typing as tp
import numpy as np

from src.utils import center_coords
from src.utils import EXTRACT_RESIDUE

class Residue:
    """
    
    """


    def __init__(self, atom_list: tp.List[str]=[], coords: tp.Union[list, np.ndarray]=[], res_name: str='RES'):
        """
        Initialize a Residue object.

        Parameters
        ----------
        atom_list : tp.List[str], optional
            The list of atom name in the residue, by default []
        coords : tp.Union[list, np.ndarray], optional
            The array of atomic coordinates of the residue, by default []
        res_name : str, optional
            The name of the residue, by default 'RES'
        """

        self.atoms = atom_list
        self.coords = coords if type(coords) == np.ndarray else np.array(coords)
        self.resname = res_name

        self._atom_id = np.arange(1, self.n_atoms + 1)
        self._res_num = 1

    @property
    def n_atoms(self)-> int:
        """
        The number of atoms in the residue.

        Returns
        -------
        int
            The number of atoms in the residue
        """
        return len(self.atoms)

    @property
    def atom_id(self)-> np.ndarray:
        """
        The array of the atom numbers of the residue in the system.

        Returns
        -------
        nd.array
            The array of the atom numbers of the residue in the system
        """
        return self._atom_id

    @atom_id.setter
    def atom_id(self, id_list: np.ndarray):
        """
        Set the atom numbers of the residue in the system.

        Parameters
        ----------
        id_list : np.ndarray
            The array of the atom numbers of the residue in the system
        """
        self._atom_id = id_list

    @property
    def res_num(self) -> int:
        """
        The number of the residue in the system.

        Returns
        -------
        int
            The number of the residue in the system
        """
        return self._res_num
    
    @res_num.setter
    def res_num(self, num):
        """
        Set the residue number in the system.

        Parameters
        ----------
        num : int
            The residue number in the system
        """
        self._res_num = num
 
    @classmethod
    def read_from_file(cls, filename, res_name: str):
        """
        Create a Residue object from a molecular file (.pdb, .mol2, .sdf).

        Parameters
        ----------
        filename : str
            The name of the residue file.
        res_name : str
            The residue name.

        Returns
        -------
        Residue
            The residue object with atomic names and coordinates from the molecular file.

        Raises
        ------
        FileNotFoundError
            The file is not found.
        ValueError
            The file format is not supported.
        """

        if os.path.exists(filename)== False:
            raise FileNotFoundError("Ligand file '{}' not found".format(filename))


        _, ext = os.path.splitext(filename)  # Residue file extension
        ext = ext.lower()  

        if ext in EXTRACT_RESIDUE:
            atoms, coordinates = EXTRACT_RESIDUE[ext](filename)  # Call the appropriate reader function
        else:
            raise ValueError(f"Unsupported file format '{ext}' for ligands.")
        
        return cls(atoms, coordinates, res_name)
    

    def centering(self):
        """
        Center the residue atomic coordinates.
        """
        
        self.coords = center_coords(self.coords)

    def copy(self):
        """
        Create a copy of the Residue object.

        Returns
        -------
        Residue
            A copy of the Residue object.
        """
        return Residue(self.atoms, self.coords, self.resname)