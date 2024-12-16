import numpy as np

def rotate

def center_coords(coords):

    center = np.mean(coords, axis=0)

    centered_coords = coords - center

    return centered_coords


def random_place_molecules(
    molecule_coords, box_dim, cutoff, num_molecules, existing_molecules=None
):
    """
    Place a series of molecules randomly in a 3D box with a minimum cutoff distance, considering existing molecules.

    Parameters:
        molecule_coords (np.ndarray): Coordinates of the molecule (Nx3 array).
        box_dim (tuple): Dimensions of the box (x, y, z).
        cutoff (float): Minimum distance between any two molecules.
        num_molecules (int): Number of molecules to place in the box.
        existing_molecules (list of np.ndarray, optional): List of existing molecules already placed in the box.

    Returns:
        list of np.ndarray: A list of placed molecule coordinates (including existing ones).
    """
    if existing_molecules is None:
        existing_molecules = []

    placed_molecules = existing_molecules.copy()  # Start with existing molecules
    box_x, box_y, box_z = box_dim

    def is_valid_placement(new_coords, placed_molecules, cutoff):
        """
        Check if the new molecule coordinates are valid by ensuring that they respect
        the minimum cutoff distance from all other placed molecules, including existing ones.
        """
        for placed in placed_molecules:
            #print(placed)
            #print(new_coords)
            distances = np.linalg.norm(new_coords[:, None, :] - placed[None, :, :], axis=-1)
            if np.any(distances < cutoff):
                return False
        return True

    while len(placed_molecules) < num_molecules + len(existing_molecules):
        # Generate random rotation using Euler angles
        theta, phi, psi = np.random.uniform(0, 2 * np.pi, size=3)
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

        # Apply rotation to the molecule coordinates
        rotated_coords = np.dot(molecule_coords, rotation_matrix.T)

        # Generate random position in the box
        random_position = np.random.uniform(0, [box_x, box_y, box_z])
        translated_coords = rotated_coords + random_position

        # Validate placement
        if is_valid_placement(translated_coords, placed_molecules, cutoff):
            placed_molecules.append(translated_coords)

    return placed_molecules
