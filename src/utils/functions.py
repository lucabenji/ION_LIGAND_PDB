"""Useful functions"""

import numpy as np

from src.utils.errors import PlacingError

# constant
Na = 6.022e23 # Avogadro number (mol^-1)

# concentration from n res
def evaluate_concentration(n: int, volume: float):
    
    conc = n/((volume*1e-27)*Na)

    return conc

# n res from concentration
def evaluate_n_from_concentration(conc: float, volume: float) -> int:

    n = conc*((volume*1e-27)*Na)

    return round(n)

# function for residue and system coordinates
def center_coords(coords):

    center = np.mean(coords, axis=0)

    centered_coords = coords - center

    return centered_coords

def rotate_coords(coords, phi, psi, theta):

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

def translate_coords(coords, vec):

    translated_coords = coords + vec

    return translated_coords

def is_valid_placement(new_coords, placed_coords, cutoff):
        
    for placed in placed_coords:
        distances = np.linalg.norm(new_coords[:, None, :] - placed[None, :, :], axis=-1)
        if np.any(distances < cutoff):
            return False
    return True

def random_place_molecules(molecule_coords, box_dim, cutoff, num, existing_coords=None):
    
    if existing_coords is None:
        existing_coords = []

    placed_coords = existing_coords.copy()  # Start with existing molecules
    box_x, box_y, box_z = box_dim

    iteration = 0
    while len(placed_coords) < num + len(existing_coords):

        if iteration > 1e4:
            msg = 'Placing molecules have exceeded 10,000 iterations.'
            raise PlacingError(msg)
        
        # Generate random rotation
        theta, phi, psi = np.random.uniform(0, 2 * np.pi, size=3)

        # Apply rotation to the molecule coordinates
        rotated_coords = rotate_coords(molecule_coords, phi, psi, theta)

        # Generate random positions inside the box
        random_position = np.random.uniform(0, [box_x, box_y, box_z])
        translated_coords = translate_coords(rotated_coords, random_position)

        # Validate placement
        if is_valid_placement(translated_coords, placed_coords, cutoff):
            placed_coords.append(translated_coords)
        
        iteration += 1

    return placed_coords

# function for pdb outfile
def write_pdb_line(atom_id: int, atom_name: str, res_name: str, res_number: int, coords: np.ndarray, 
                   alternate_location=' ', chain_id=' ', element=' ') -> str:
    
    format_line = (
        "ATOM  {atom_id:5d} {atom_name:>3s}{alternate_location} {residue_name:<3s} {chain_id}{residue_number:4d}    "
        "{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {element:>2}"
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