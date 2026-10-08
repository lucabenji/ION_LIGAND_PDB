"""
Module containing useful functions for placing residues and writing pdb files.
"""

from datetime import datetime
import numpy as np
from typing import Optional, List

from src.utils.errors import PlacingError

# constant
Na = 6.022e23 # Avogadro number (mol^-1)

# concentration from n res
def evaluate_concentration(n: int, volume: float) -> float:
    """
    Evaluate the molar concentration in a volume from the number of residues.

    Parameters
    ----------
    n : int
        Number of residues.
    volume : float
        System volume (in Ang^3).

    Returns
    -------
    float
        The residue concentration.
    """
    
    conc = n/((volume*1e-27)*Na)

    return conc

# n res from concentration
def evaluate_n_from_concentration(conc: float, volume: float) -> int:
    """
    Evaluate the number of residues from their concentration in a given volume.

    Parameters
    ----------
    conc : float
        Residue concentration.
    volume : float
        System volume (in Ang^3).

    Returns
    -------
    int
        Number of residues.
    """

    n = conc*((volume*1e-27)*Na)

    return round(n)

# function for residue and system coordinates
def center_coords(coords: np.ndarray) ->np.ndarray:
    """
    Center a 3D set of coordinates.

    Parameters
    ----------
    coords : np.ndarray
        3D coordinates.

    Returns
    -------
    np.ndarray
        Centered coordinates.
    """

    center = np.mean(coords, axis=0)

    centered_coords = coords - center

    return centered_coords

def rotate_coords(coords:np.ndarray, phi: float, psi: float, theta: float)-> np.ndarray:
    """
    Rotate a 3D set of coordinates

    Parameters
    ----------
    coords : np.ndarray
        3D coordinates.
    phi : float
        Rotation angle around X (in rad).
    psi : float
        Rotation angle around Y (in rad).
    theta : float
        Rotation angle around Z (in rad).

    Returns
    -------
    np.ndarray
        Rotated coordinates.
    """

    rotation_matrix = np.array([
            [
                np.cos(psi) * np.cos(phi) - np.sin(psi) * np.cos(theta) * np.sin(phi),
                -np.sin(psi) * np.cos(phi) - np.cos(psi) * np.cos(theta) * np.sin(phi),
                np.sin(theta) * np.sin(phi),
            ],
            [
                np.cos(psi) * np.sin(phi) + np.sin(psi) * np.cos(theta) * np.cos(phi),
                -np.sin(psi) * np.sin(phi) + np.cos(psi) * np.cos(theta) * np.cos(phi),
                -np.sin(theta) * np.cos(phi),
            ],
            [
                np.sin(psi) * np.sin(theta),
                np.cos(psi) * np.sin(theta),
                np.cos(theta),
            ],
        ])
    
    rotated_coords = np.dot(coords, rotation_matrix.T)

    return rotated_coords

def translate_coords(coords: np.ndarray, vec: np.ndarray) -> np.ndarray:
    """
    Translate a set of 3D coordinates.

    Parameters
    ----------
    coords : np.ndarray
        3D coordinates.
    vec : np.ndarray
        Translation vector.

    Returns
    -------
    np.ndarray
        Translated coordinates.
    """
    translated_coords = coords + vec

    return translated_coords

def is_valid_placement(new_coords: np.ndarray, placed_coords: List[np.ndarray], cutoff: float) -> bool:
    """
    Check if a new set of 3D coordinates respects the cutoff distance with the present ones.

    Parameters
    ----------
    new_coords : np.ndarray
        New set of 3D coordinates.
    placed_coords : List
        List of present coordinates. 
    cutoff : float
        Cutoff distance.

    Returns
    -------
    bool
        True if the new coordinates respect the cutoff distance.
    """
        
    for placed in placed_coords:
        distances = np.linalg.norm(new_coords[:, None, :] - placed[None, :, :], axis=-1)

        if np.any(distances < cutoff):
            return False
        
    return True

def random_place_molecules(molecule_coords: np.ndarray, box_dim: np.ndarray, cutoff: float, num: int, existing_coords:Optional[List] = None) -> List:
    """
    Place randomly sets a set of coordinates inside a box. A minimum distance (cutoff) between new coordinates and alredy present ones must be specified.

    Parameters
    ----------
    molecule_coords : np.ndarray
        3D set of coordinates to locate in the system.
    box_dim : np.ndarray
        (3, ) array of the system dimension box.
    cutoff : float
        Minimum required distance between new molecules and the existing ones. 
    num : int
        Number of new set of coordinates that have to be placed.
    existing_coords : Optional[List], optional
        Coordinates alredy present in the system, by default None.

    Returns
    -------
    List
        Coordinates present in the system (new + old ones).

    Raises
    ------
    PlacingError
        Number of iteration needed to allocate all new coordinates has exceed 10000.
    """
    
    if existing_coords is None:
        existing_coords = []

    # Start with existing molecules
    placed_coords = existing_coords.copy()  
    box_x, box_y, box_z = box_dim

    iteration = 0
    while len(placed_coords) < num + len(existing_coords):

        if iteration > 1e4:
            msg = 'Placing molecules have exceeded 10,000 iterations.'
            raise PlacingError(msg)
        
        # Random rotation angle
        theta, phi, psi = np.random.uniform(0, 2 * np.pi, size=3)

        # Random rotation to new coordinates
        rotated_coords = rotate_coords(molecule_coords, phi, psi, theta)

        # Random positions inside the box
        random_position = np.random.uniform(0, [box_x, box_y, box_z])
        translated_coords = translate_coords(rotated_coords, random_position)

        # Validate placement
        if is_valid_placement(translated_coords, placed_coords, cutoff):
            placed_coords.append(translated_coords)
        
        # Iteration count
        iteration += 1

    return placed_coords

# Function for pdb file

def write_pdb_header(box: np.ndarray) -> List[str]:
    """
   Generate a list of strings for a PDB file header.
   1st line is HEADER section with datetime.
   2nd line contains AUTHOR name.
   3rd line contains box information.

    Parameters
    ----------
    box : np.ndarray
        System box dimension in a (3, ) array.

    Returns
    -------
    List[str]
        List of header lines.
    """

    header_lines = []
    

    # HEADER
    date = datetime.now().strftime("%d-%b-%y").upper()
    header = "HEADER    {:40}{:>9}\n".format('', date)

    header_lines.append(header)

    #AUTHOR
    author = 'AUTHOR ION_LIGAND_PDB\n'

    header_lines.append(author)

    #CRYST1
    # only cubic/rectangular box are supported
    cryst_line = '\nCRYST1{:9.3f}{:9.3f}{:9.3f}{:7.2f}{:7.2f}{:7.2f}\n'.format(box[0], box[1], box[2], 90.0, 90.0, 90,0)

    header_lines.append(cryst_line)

    return header_lines



def write_pdb_line(atom_id: int, atom_name: str, res_name: str, res_number: int, coords: np.ndarray, 
                   alternate_location=' ', chain_id=' ', element=' ') -> str:
    """
    Generate a correctly formatted PDB file line from atom information.

    Parameters
    ----------
    atom_id : int
        Index of the atom in the system.
    atom_name : str
        Name of the atom.
    res_name : str
        Residue name.
    res_number : int
        Index of the residue in the system.
    coords : np.ndarray
        Coordinates of the atom in a (3, ) array.
    alternate_location : str, optional
       Alternative locations of the atom, by default ' '
    chain_id : str, optional
        Index of the chain where the atom belongs, by default ' '
    element : str, optional
        Element of the atom from the periodic table, by default ' '

    Returns
    -------
    str
        Formatted PDB file line.
    """
    
    format_line = (
        "ATOM  {atom_id:5d} {atom_name:>3s}{alternate_location} {residue_name:<3s} {chain_id}{residue_number:4d}    "
        "{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {element:>2}\n"
    )

    pdb_line = format_line.format(  atom_id=atom_id, 
                                    atom_name=atom_name, 
                                    alternate_location=alternate_location, 
                                    residue_name=res_name,
                                    chain_id = chain_id,
                                    residue_number = res_number+1,
                                    x = coords[0],
                                    y = coords[1],
                                    z = coords[2],
                                    element = element
                                    )
    
    return pdb_line