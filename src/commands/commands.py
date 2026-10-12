"""
Module containing all the available commands of ION_LIGAND_PDB program.

All commands take as arguments 'args' since they act on arguments parsed by src.parsing.parsing module.
"""

import numpy as np
import sys

from src import Residue
from src import System

from src.utils.functions import evaluate_n_from_concentration
from src.utils.errors import ExecutionError, LigandFileError, PlacingError,  BoxError
from src.utils.fancy_print import end

# System object where all the commands are acting.
Syst = System()


def add_ion(args):
    """
    Add ion to the system.
    """

    ion_coords = np.array([[0.0, 0.0, 0.0]])
    
    ion_name = args.ION
    cutoff = args.cutoff

    print('\nAdding ion with name {} using cutoff {:.2f} Ang\n'.format(ion_name, cutoff))

    # error if cutoff is more then system dimensions
    if np.any(cutoff > Syst.box):
        msg = 'Required cutoff is {:.2f} but system dimensions is {:.2f}x{:.2f}x{:.2f} Ang.'.format(cutoff, Syst.box[0], Syst.box[1], Syst.box[2])
        raise ExecutionError(message=msg)

    # ion name too long
    if len(ion_name) > 3:
        print('Warning! Ion name {} exceeds maximum number of 3 characters. \nIon name will be shortened to {}\n.'.format(ion_name, ion_name[:3]))
        ion_name = ion_name[:3]
    
    # crate Residue obj. for ion
    ion = Residue(atom_list=[ion_name], coords=ion_coords, res_name=ion_name)
    
    # number of ions to add
    n = args.N
    if args.conc:
        n =  evaluate_n_from_concentration(args.conc, Syst.volume) - Syst._get_number_of_res(ion.resname)
        # error if n <= 0
        if n <= 0:
            msg = 'The user asked for concentration {:.2f}, but {} concentration is {:.2f}. \nTry to increase the system volume.'.format(args.conc, 
                                                                                                                                         ion.resname, 
                                                                                                                                         Syst._get_res_concentration(ion.resname))          
            raise ExecutionError(message=msg)
            
    # add ions to system
    print('\nAdding {} ions.'.format(n))
    try:
        Syst.add_residue(res=ion, cutoff=cutoff, n=n)
    # error when placing molecules
    except PlacingError as e:
        msg = '{}\n Try to reduce the cutoff or increase system volume.'.format(e.message)
        raise ExecutionError(message=msg)
    
    print('Final {} concentration is: {:.2f} M\n.'.format(ion.resname, Syst._get_res_concentration(ion.resname)))


def add_ligand(args):
    """
    Add ligand to the system.
    """
    
    res_name = args.LIG
    cutoff = args.cutoff

    print('\nAdding ligand with name {} using cutoff {:.2f} Ang\n'.format(res_name, cutoff))

    # ligand resname too long
    if len(res_name) > 3:
        print('Warning! Ligand residue name {} exceeds maximum number of 3 characters. Ligand residue name will be shortened to {}\n.'.format(res_name, res_name[:3]))
        res_name = res_name[:3]
    
    # error if cutoff is more then system dimensions
    if np.any(cutoff > Syst.box):
        msg = 'Required cutoff is {:.2f} but system dimensions is {:.2f}x{:.2f}x{:.2f} Ang.'.format(cutoff, Syst.box[0], Syst.box[1], Syst.box[2])
        raise ExecutionError(message=msg)
    
    # create Residue obj. for ligand
    lig_file = args.file_name
    print('Reading ligand from file {}.'.format(lig_file))
    try:
        lig = Residue.read_from_file(filename=lig_file, res_name=res_name)
    except LigandFileError as e:
        msg(f'Error with file {e.filename}. {e.message}')
        raise ExecutionError(message=msg)

    n = args.N
    if args.conc:
        n =  evaluate_n_from_concentration(args.conc, Syst.volume) - Syst._get_number_of_res(lig.resname)
        # error if n <= 0
        if n <= 0:
            msg = 'The user asked for concentration {:.2f} M, but {} concentration is {:.2f} M. Try to increase the system volume.'.format(args.conc, 
                                                                                                                                           lig.resname, 
                                                                                                                                           Syst._get_res_concentration(lig.resname))          
            raise ExecutionError(message=msg)

    # add ligand to system
    print('Adding {} ligands\n.'.format(n))
    try:
        Syst.add_residue(res=lig, cutoff = cutoff, n=n)
    # error when placing ligands
    except PlacingError as e:
        msg = '{}\n Try to reduce the cutoff or increase system volume.'.format(e.message)
        raise ExecutionError(message=msg)

    print('Final {} concentration is: {:.3f} M.\n'.format(lig.resname, Syst._get_res_concentration(lig.resname)))

def generate_pdb(args):
    """
    Generate the PDB file of the system.
    """
    filename = args.pdb_file
    
    if Syst.is_empty:
        msg = 'System is empty! Can not generate the PDB file.'
        raise ExecutionError(message=msg)
    else:
        Syst.generate_pdb(filename)
        print('System saved in {}'.format(filename))


def quit(args):
    """
    Exit the program.
    """
    end()
    sys.exit()

def remove(args):
    """
    Remove a residue from the system.
    """
    # error if no residue to remove
    if Syst.is_empty:
        msg = 'System is empty! Can not remove any residue.'
        raise ExecutionError(message=msg)

    resname = args.RES

    # remove all residue
    if resname == 'all':
        print('\nRemoving all residues from the system.')
        Syst.residues = []
        print('System is now empty.\n')

    elif Syst.residue_exists(resname):
        Syst.remove_residue(resname)
        print('\nResidue {} has been removed from the system.'.format(resname))

    else:
        msg = f'No residue with name {resname} has been found.'
        raise ExecutionError(message=msg)

def set_box(args):
    """
    Set the box dimension of the system (in Ang).
    """
    dim = args.DIM
    print('\nSetting system cubic box dimension to {:.1f} Ang.'.format(dim = args.DIM))
    # generate cubic box
    box = np.array([dim, dim, dim])

    try: 
        Syst.box = box
    # problem with box setting
    except BoxError as e:
        msg = e.message
        raise ExecutionError(message=msg)


def set_volume(args):
    """
    Set the volume of the system (in Ang^3).
    """

    volume = args.VOL
    dim = volume**(1/3)

    print('\nRequested volume is {:.2f} Ang^3. \nSetting system cubic box dimension to {:.1f} Ang.'.format(volume, dim))
    box = np.array([dim, dim, dim])

    try: 
        Syst.box = box
    # problem with box setting
    except BoxError as e:
        msg = e.message
        raise ExecutionError(message=msg)