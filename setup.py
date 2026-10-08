import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='ion_ligand_pdb',
    version='0.0.1',
    author='Luca Benedetti',
    author_email = 'luca.benedetti@sns.it',
    description='Ion-ligand PDB file generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(include=[
        'src.__init__',
        'src.System',
        'src.Residue',
        'src.commands.commands',
        'src.commands.execution',
        'src.parser.parser',
        'src.parser.input'
        'src.utils.errors'
        'src.utils.file_reader'
        'src.utils.function'        
    ]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    python_requires='>=3.10',
    install_requires=[
        'numpy>=3.0'
    ],
    entry_points={
        'console_scripts': [
            'ion_ligand_pdb=main:main',
        ],
    },
)
