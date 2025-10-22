"""
Available commands
"""

import numpy as np
import sys

from src import Residue
from src import System

from src.utils import evaluate_n_from_concentration

Syst = System()

def add_ion(args):
    """
    """

    ion_coords = np.array([[0.0, 0.0, 0.0]])
    ion_name = args.ION
    ion = Residue(atom_list=[ion_name], coords=ion_coords, res_name=ion_name)
    
    n = args.n
    if args.conc:
        n =  evaluate_n_from_concentration(args.conc, Syst.volume) - Syst.get_number_of_res(ion_name)
        print('\nSelected concentration for ion {}: {:.3f} M.'.format(ion_name, args.conc))
    cutoff = args.cutoff
    Syst.add_residue(res=ion, cutoff=cutoff, n=n)
    
    print('\nAdded {} ion(s) with name {} using cutoff {:.2f} Ang'.format(n, ion.resname, cutoff))
    print('Ion concentration is: {:.3f} M.'.format(Syst.get_res_concentration(ion_name)))

def add_ligand(args):
    """
    """

    lig_file = args.file_name
    n = args.n
    res_name = args.RES
    cutoff = args.cutoff

    lig = Residue.read_from_file(filename=lig_file, res_name=res_name)

    Syst.add_residue(res=lig, cutoff = cutoff, n=n)

    print('\nAdded {} ligand(s) with residue name {} using cutoff {:.2f} Ang'.format(n, lig.resname, cutoff))

def generate_pdb(args):
    """
    """
    
    Syst.generate_pdb()


def quit(args):
    """
    """
    print('Goodbye!')
    sys.exit()

def remove_ion(args):

    resname = args.ION
    
    Syst.remove_residue(resname)

    print('\n Ions {} have been removed from the system.'.format(resname))

def remove_ligand(args):

    resname = args.LIG
    
    Syst.remove_residue(resname)

    print('\n Ligands {} have been removed from the system.'.format(resname))


def set_box(args):
    """
    """

    dim = args.DIM
    box = np.array([dim, dim, dim])

    Syst.box = box
    
    print('\nSystem has now a square box of edge {:.2f} Ang ({:.2f} nm).'.format(dim, dim/10))
    print('Volume is {:.2f} Ang^3 ({:.2f} nm^3).'.format(Syst.volume, Syst.volume/1000))

def set_volume(args):

    volume = args.VOL
    dim = volume**(1/3)
    box = np.array([dim, dim, dim])

    Syst.box = box
    print('\nSystem has now a box volume of {:.2f} Ang^3 ({:.2f} nm^3).'.format(Syst.volume, Syst.volume/1000))
    print('Edge is {:.2f} Ang ({:.2f} nm).'.format(dim, dim/10))