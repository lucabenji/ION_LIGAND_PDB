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

Commands can be given through an input file or directly from the terminal, after the program is lauched.

## Available commands

- **add_ion**

    ```bash
    add_ion [-h] [-cutoff CUTOFF] [-n N | -conc CONC] ION
    ```

- **add_ligand**

    ```bash
    add_ligand [-h] -f FILE_NAME [-cutoff CUTOFF] [-n N | -conc CONC] [LIG]
    ```

- **generate_pdb**

    ```bash
    generate_pdb [-h] PDB_FILE
    ```

- **quit**

    ```bash
    quit
    ```

- **remove**

    ```bash
    remove [-h] RES | all
    ```

- **set_box**

    ```bash
    set_box [-h] DIM
    ```

- **set_volume**

    ```bash
    set_volume [-h] VOL
    ```

## Examples
