# ION_LIGAND_PDB

## Description

ION_LIGAND_PDB is a Python-based program for generating Protein Data Bank (PDB) files of metal ion–ligand systems.

The program is designed for researchers who need to build metal ion–ligand systems for molecular dynamics (MD) simulations, as well as for other computational chemistry and molecular modeling applications.

Users can specify any metal ion and provide ligands in common molecular file formats, including PDB, MOL2, and SDF. The program allows users to customize key system parameters, such as ion/ligand concentrations and simulation box dimensions.

The resulting PDB files can be readily used as input for generating topology and coordinate files with widely used MD simulation packages, including AMBER, GROMACS, and NAMD.

Generated structures can also be inspected and visualized using popular molecular visualization programs such as Chimera, PyMOL, and VMD.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Available commands](#available-commands)
- [Examples](#examples)

## Features

- **Get ligand from common molecular file formats** - Select ligands from PDB (.pdb), MOL2 (.mol2), and SDF (.sdf) files

- **Customize ion/ligand number and concentration** - Select the preferred number or concentration of ion/ligand in your system.

- **Choose system box dimension and volume for MD simulations** - Customize system box for your simulations

- **Generate PDB files for topology and input coordinates** - Obtained PDB files are readily usable for generating topology and input coordinates in most used MD softwares.

- **Visualize new PDBs with common molecular visualizers** - Obtained PDB files can be visualized with Chimera, PyMOL, VMD, etc.

## Installation

1. Clone the repository:  

    ```bash
    git clone https://github.com/lucabenji/ION_LIGAND_PDB.git
    cd ION_LIGAND_PDB
    ```

2. Install the program (as editable):  

    ```bash
    pip install -e .
    ```

3. Launch the program:

    ```bash
    ion_ligand_pdb
    ```

## Usage

ION_LIGAND_PDB works with commands provided by the user. Commands follow the syntax:

```bash
> command keyword
```

Commands can be given through two different operative mode:

1. **Input file mode**

    ```bash
    ion_ligand_pdb -i input.in        
    ```

    User can provide commands from an input file with all the istructions.

2. **Interactive mode**

    ```bash
    ion_ligand_pdb
    ```

    If no input file is provided, commands can be given directly from the terminal.

## Available commands

- **add_ion**

    ```bash
    add_ion [-h] [-cutoff CUTOFF] [-n N | -conc CONC] ION
    ```

    Select the ion and its quantity. The user must provide the ion name, with maximum 3 characters.  
    The user can also select the number of ions or its molar concentration. Default value is 1 ion.  
    Ions will be randomly placed inside the system, with a minimum distance between other residues specified by CUTOFF (default is 4.0 Ang).

- **add_ligand**

    ```bash
    add_ligand [-h] -f FILE_NAME [-cutoff CUTOFF] [-n N | -conc CONC] [LIG]
    ```

    Select the ligand molecule and its quantity. The ligand PDB, SDF or mol2 file must be provided.  
    The user can specify the ligand number or its concentration. Default value is 1 ligand molecule.  
    A residue name can be provided with maximum three characters. If not, the default LIG name will be used.  
    Ligands will be randomly placed inside the system, with a minimum distance between other residues specified by CUTOFF (default is 4.0 Ang).

- **generate_pdb**

    ```bash
    generate_pdb [-h] PDB_FILE.pdb
    ```

    Generate the PDB file with name PDB_FILE.pdb.

- **quit**

    ```bash
    quit
    ```

    Exit the program.

- **remove**

    ```bash
    remove [-h] RES | all
    ```

    Remove residues (ion or ligand) from the system. RES is the residue name of the residue to be removed.  
    If 'all' is specified, all residues will be removed.

- **set_box**

    ```bash
    set_box [-h] DIM
    ```

    Set the system square box edge dimension in Ang.

- **set_volume**

    ```bash
    set_volume [-h] VOL
    ```

## Examples

Some examples are provided in the directory 'examples/'.
After the istallation, do:

```bash
cd examples/
ion_ligand_pdb -i example1.in #Generate the pdb for a system with 4 Ni ion and 10 NME in a 4x4x4 nm box
ion_ligand_pdb -i example2.in #Generate the pdb for a system with 0.5 M of Ca and 0.1 M of EDTA in a 144 nm^3 box 
```
