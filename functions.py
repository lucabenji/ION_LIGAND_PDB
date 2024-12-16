"""Useful functions"""

import numpy as np


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

def random_place_molecules(coords, box_dim, cutoff, num, existing_coords=None):
    
    if existing_coords is None:
        existing_coords = []

    placed_coords = existing_coords.copy()  # Start with existing molecules
    box_x, box_y, box_z = box_dim

    def is_valid_placement(new_coords, placed_coords, cutoff):
        
        for placed in placed_coords:
            #print(placed)
            #print(new_coords)
            distances = np.linalg.norm(new_coords[:, None, :] - placed[None, :, :], axis=-1)
            if np.any(distances < cutoff):
                return False
        return True

    while len(placed_coords) < num + len(existing_coords):
        
        # Generate random rotation using Euler angles
        theta, phi, psi = np.random.uniform(0, 2 * np.pi, size=3)

        # Apply rotation to the molecule coordinates
        rotated_coords = rotate_coords(coords, phi, psi, theta)

        # Generate random position in the box
        random_position = np.random.uniform(0, [box_x, box_y, box_z])
        translated_coords = translate_coords(rotated_coords, random_position)

        # Validate placement
        if is_valid_placement(translated_coords, placed_coords, cutoff):
            placed_coords.append(translated_coords)

    return placed_coords
