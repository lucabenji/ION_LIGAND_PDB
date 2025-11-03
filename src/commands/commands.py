"""
Available commands on ION_LIGAND_PDB.
"""

import numpy as np
import sys

from src import Residue
from src import System

from src.utils import evaluate_n_from_concentration
from src.utils import CommandError

# generate system
Syst = System()

def add_ion(args):
    """
    Add ion to System.
    """

    ion_coords = np.array([[0.0, 0.0, 0.0]])
    
    ion_name = args.ION
    cutoff = args.cutoff

    # ion name too long
    if len(ion_name) > 3:
        print('Warning! Ion name {} exceeds maximum number of 3 characters. Ion name will be shortened to {}'.format(ion_name, ion_name[:3]))
        ion_name = ion_name[:3]
    
    # crate Residue obj. for ion
    ion = Residue(atom_list=[ion_name], coords=ion_coords, res_name=ion_name)
    
    # number of ions to add
    n = args.n
    if args.conc:
        n =  evaluate_n_from_concentration(args.conc, Syst.volume) - Syst.get_number_of_res(ion.resname)
        # error if n <= 0
        if n <= 0:
            msg = 'The user asked for concentration {:.3f}, but {} concentration is {:.3f}. Try to increase the system volume.'.format(args.conc, ion.resname, Syst.get_res_concentration(ion.resname))          
            raise CommandError(command='add_ion', message=msg)
            
    

    # add ions to system
    Syst.add_residue(res=ion, cutoff=cutoff, n=n)
    
    print('\nAdded {} ion(s) with name {} using cutoff {:.2f} Ang'.format(n, ion.resname, cutoff))
    print('{} concentration is: {:.3f} M.'.format(ion.resname, Syst.get_res_concentration(ion.resname)))

def add_ligand(args):
    """
    Add ligand to System.
    """

    lig_file = args.file_name
    res_name = args.RES

    # ligand resname too long
    if len(res_name) > 3:
        print('Warning! Ligand residue name {} exceeds maximum number of 3 characters. Ligand residue name will be shortened to {}'.format(res_name, res_name[:3]))
        res_name = res_name[:3]
    cutoff = args.cutoff

    # create Residue obj. for ligand
    lig = Residue.read_from_file(filename=lig_file, res_name=res_name)

    n = args.n
    if args.conc:
        n =  evaluate_n_from_concentration(args.conc, Syst.volume) - Syst.get_number_of_res(lig.resname)
        if args.conc:
            n =  evaluate_n_from_concentration(args.conc, Syst.volume) - Syst.get_number_of_res(lig.resname)
        # error if n <= 0
        if n <= 0:
            msg = 'The user asked for concentration {:.3f} M, but {} concentration is {:.3f} M. Try to increase the system volume.'.format(args.conc, lig.resname, Syst.get_res_concentration(lig.resname))          
            raise CommandError(command='add_ion', message=msg)
    cutoff = args.cutoff

    Syst.add_residue(res=lig, cutoff = cutoff, n=n)

    print('\nAdded {} ligand(s) with residue name {} using cutoff {:.2f} Ang'.format(n, lig.resname, cutoff))
    print('{} concentration is: {:.3f} M.'.format(lig.resname, Syst.get_res_concentration(lig.resname)))

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