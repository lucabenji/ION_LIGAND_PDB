"""
Residue module.

It contain the Residue class, used to generate ions or ligands
"""
import os

import typing as tp
import numpy as np

from src.utils import center_coords
from src.utils import EXTRACT_RESIDUE

from src.utils import LigandFileError

class Residue:
    """
    Residue
    -------

    Generate a residue istance for an ion or a ligand.

    Attributes
    ----------
    atom_list : tp.List[str], optional
        The list of atom name in the residue, by default []
    coords : tp.Union[list, np.ndarray], optional
        The array of atomic coordinates of the residue, by default []
    res_name : str, optional
        The name of the residue, by default 'RES'
    
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
        return self.__atom_id

    @atom_id.setter
    def atom_id(self, id_list: np.ndarray):
        """
        Set the atom numbers of the residue in the system.

        Parameters
        ----------
        id_list : np.ndarray
            The array of the atom numbers of the residue in the system
        """
        self.__atom_id = id_list

    @property
    def res_num(self) -> int:
        """
        The number of the residue in the system.

        Returns
        -------
        int
            The number of the residue in the system
        """
        return self.__res_num
    
    @res_num.setter
    def res_num(self, num):
        """
        Set the residue number in the system.

        Parameters
        ----------
        num : int
            The residue number in the system
        """
        self.__res_num = num
 
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
        LigandFileError
            The file is not found.
        LigandFileError
            The file format is not supported.
        """

        # File not found
        if os.path.exists(filename)== False:
            msg = "Ligand file '{}' not found.".format(filename)
            raise LigandFileError(filename, msg)


         # Residue file extension
        _, ext = os.path.splitext(filename) 
        ext = ext.lower()  

        # Call the appropriate reader function
        if ext in EXTRACT_RESIDUE:
            atoms, coordinates = EXTRACT_RESIDUE[ext](filename) 
        # unsupported file format
        else:
            msg = f"Unsupported file format '{ext}' for ligand files."
            raise LigandFileError(filename, msg)
        
        return cls(atoms, coordinates, res_name)
    

    def centering(self):
        """
        Center the residue atomic coordinates.
        """
        
        self.coords = center_coords(self.coords)
    
    def copy(self):
        """
        Create a copy of a Residue object.

        Returns
        -------
        Residue
            A copy of the Residue object.
        """
        return Residue(self.atoms, self.coords, self.resname)