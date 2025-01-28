"""
Available commands
"""

import numpy as np
import sys

from residue import Residue
from system import System


System = System()

def add_ion(args):
    """
    """

    ion_name = args.ION
    n = args.n
    cutoff = args.cutoff 

    #if args.coords:
    #    ion_coords = args.coords
    #else:
    ion_coords = np.array([[0.0, 0.0, 0.0]]) 

    ion = Residue(atom_list=[ion_name], coords=ion_coords, res_name=ion_name)

    System.add_residue(res=ion, cutoff=cutoff, n=n)
    
    print('\nAdded {} ion(s) with name {} using cutoff {:.2f} Ang'.format(n, ion.resname, cutoff))

def add_ligand(args):
    """
    """

    lig_file = args.file_name
    n = args.n
    res_name = args.RES
    cutoff = args.cutoff

    lig = Residue.read_from_pdb(filename=lig_file, res_name=res_name)

    System.add_residue(res=lig, cutoff = cutoff, n=n)

    print('\nAdded {} ligand(s) with residue name {} using cutoff {:.2f} Ang'.format(n, lig.resname, cutoff))

def generate_pdb(args):
    """
    """
    
    System.generate_pdb()


def quit(args):
    """
    """
    print('Goodbye!')
    sys.exit()

def set_box(args):
    """
    """

    dim = args.DIM
    box = np.array([dim, dim, dim])

    System.box = box
    
    print('\nSystem has now a square box of {:.2f} Ang ({:.2f} nm).'.format(dim, dim/10))
    print('Volume is {:.2f} Ang^3 ({:.2f} nm^3).'.format(System.volume, System.volume/1000))

def set_volume(args):

    volume = args.VOL
    dim = volume**(1/3)
    box = box = np.array([dim, dim, dim])

    System.box = box
    print('\nSystem has now a box volume of {:.2f} Ang^3 ({:.2f} nm^3).'.format(System.volume, System.volume/1000))
    print('Edge is {:.2f} Ang ({:.2f} nm).'.format(dim, dim/10))