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
        'src.System',
        'src.Residue',
        'src.commands',
        'srcexecution',
        'src.parser',
        'src.utils.errors',
        'src.utils.file_reader',
        'src.utils.function'        
    ]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Molecular Dynamics'
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.0'
    ],
    entry_points={
        'console_scripts': [
            'ion_ligand_pdb=main:main',
        ],
    },
)
