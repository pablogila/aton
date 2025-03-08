<p align="center"><img width="40.0%" src="pics/aton.png"></p>


# Welcome to ATON

The **A**b-ini**T**i**O** & **N**eutron research toolbox,
or [ATON](https://pablogila.github.io/ATON/),
provides powerful and comprehensive tools
for cutting-edge materials research,
focused on (but not limited to) neutron science.
Designed to bridge the gap between theoretical modeling and experimental validation,
ATON allows researchers to streamline and simplify workflows in the study of advanced materials.

Just like its [ancient Egyptian deity](https://en.wikipedia.org/wiki/Aten) counterpart,
this all-in-one Python package comprises a range of utility tools
from INS spectra analysis to *ab-initio* interfaces
for [Quantum ESPRESSO](https://www.quantum-espresso.org/),
[Phonopy](https://phonopy.github.io/phonopy/) and
[CASTEP](https://castep-docs.github.io/castep-docs/).
Conversion factors and universal constants from the [2022 CODATA](https://doi.org/10.48550/arXiv.2409.03787)
Recommended Values of the Fundamental Physical Constants are also included.  

The source code is available on [GitHub](https://github.com/pablogila/ATON/).   
Check the [full documentation online](https://pablogila.github.io/ATON/).  


---


# Installation

As always, it is recommended to install your packages in a virtual environment:  
```bash
python3 -m venv .venv
source .venv/bin/activate
```


## With pip

Install ATON with  
```bash
pip install aton
```

Or upgrade to a new version as
```bash
pip install aton -U
```


## From source

Optionally, you can install ATON from the [GitHub repo](https://github.com/pablogila/ATON/).
Clone the repository or download the [latest stable release](https://github.com/pablogila/ATON/tags)
as a ZIP, unzip it, and run inside the `ATON/` directory:  
```bash
pip install .
```


---


# Documentation

The full ATON documentation is available [online](https://pablogila.github.io/ATON/).  
An offline version is found at `docs/aton.html`.  
Code examples are included in the [`examples/`](https://github.com/pablogila/ATON/tree/main/examples) folder.    


## Interfaces for *ab-initio* codes

The **interface** module contains Python interfaces for several *ab-initio* codes.
These are powered by the [aton.txt](#general-text-edition) module and can be easily extended.

### [aton.interface](https://pablogila.github.io/ATON/aton/interface.html)

| | |  
| --- | --- |  
| [interface.qe](https://pablogila.github.io/ATON/aton/interface/qe.html)           | Interface for [Quantum ESPRESSO](https://www.quantum-espresso.org/)'s [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) module |  
| [interface.phonopy](https://pablogila.github.io/ATON/aton/interface/phonopy.html) | Interface for [Phonopy](https://phonopy.github.io/phonopy/) calculations |  
| [interface.castep](https://pablogila.github.io/ATON/aton/interface/castep.html)   | Interface for [CASTEP](https://castep-docs.github.io/castep-docs/) calculations |  
| [interface.slurm](https://pablogila.github.io/ATON/aton/interface/slurm.html) | Batch jobs via [Slurm](https://slurm.schedmd.com/) |


## Physico-chemical constants

The **phys** module contains physical constants and conversion factors,
as well as chemical information from all known elements.
Values are accessed directly as `phys.value` or `phys.function()`.

### [aton.phys](https://pablogila.github.io/ATON/aton/phys.html)

| | |  
| --- | --- |  
| [phys.units](https://pablogila.github.io/ATON/aton/phys/units.html)         | Physical constants and conversion factors |  
| [phys.atoms](https://pablogila.github.io/ATON/aton/phys/atoms.html)         | Megadictionary with data for all chemical elements |  
| [phys.functions](https://pablogila.github.io/ATON/aton/phys/functions.html) | Functions to sort and analyse element data |  


## Quantum rotations

The **QRotor** module is used to study energy excitations and tunnel splittings
from molecular rotations, such as those of methyl and amine groups.

### [aton.qrotor](https://pablogila.github.io/ATON/aton/qrotor.html)

| | |
| --- | --- |
| [qrotor.system](https://pablogila.github.io/ATON/aton/qrotor/system.html)       | Definition of the quantum `System` object |
| [qrotor.systems](https://pablogila.github.io/ATON/aton/qrotor/systems.html)     | Functions to manage several System objects |
| [qrotor.rotate](https://pablogila.github.io/ATON/aton/qrotor/rotate.html)       | Rotate specific atoms from structural files |
| [qrotor.constants](https://pablogila.github.io/ATON/aton/qrotor/constants.html) | Common bond lengths and inertias |
| [qrotor.potential](https://pablogila.github.io/ATON/aton/qrotor/potential.html) | Potential definitions and loading functions |
| [qrotor.solve](https://pablogila.github.io/ATON/aton/qrotor/solve.html)         | Solve rotation eigenvalues and eigenvectors |
| [qrotor.plot](https://pablogila.github.io/ATON/aton/qrotor/plot.html)           | Plotting functions |


## Spectra analysis

The **spx** module includes tools for spectral analysis from
Inelastic Neutron Scattering, Raman, Infrared, etc.

### [aton.spx](https://pablogila.github.io/ATON/aton/spx.html)

| | |  
| --- | --- |  
| [spx.classes](https://pablogila.github.io/ATON/aton/spx/classes.html)     | Class definitions for the spectra module |  
| [spx.fit](https://pablogila.github.io/ATON/aton/spx/fit.html)             | Spectra fitting functions |  
| [spx.normalize](https://pablogila.github.io/ATON/aton/spx/normalize.html) | Spectra normalization |  
| [spx.plot](https://pablogila.github.io/ATON/aton/spx/plot.html)           | Plotting |  
| [spx.deuterium](https://pablogila.github.io/ATON/aton/spx/deuterium.html) | Deuteration estimations via INS |  
| [spx.samples](https://pablogila.github.io/ATON/aton/spx/samples.html)     | Sample materials for testing |  


## General text edition

The **txt** module handles text files.
It powers more complex subpackages,
such as [aton.interface](#interfaces-for-ab-initio-codes).

### [aton.txt](https://pablogila.github.io/ATON/aton/txt.html)

| | |  
| --- | --- |  
| [txt.find](https://pablogila.github.io/ATON/aton/txt/find.html)       | Search for specific content in text files |  
| [txt.edit](https://pablogila.github.io/ATON/aton/txt/edit.html)       | Manipulate text files |  
| [txt.extract](https://pablogila.github.io/ATON/aton/txt/extract.html) | Extract data from raw text strings |  


## System tools

Additional utility tools are available for common system tasks across subpackages.

| | |  
| --- | --- |  
| [aton.file](https://pablogila.github.io/ATON/aton/file.html)   | File manipulation |  
| [aton.alias](https://pablogila.github.io/ATON/aton/alias.html) | Useful dictionaries for user input correction |  
| [aton.call](https://pablogila.github.io/ATON/aton/call.html)   | Run bash scripts and related |   


---


# Contributing

If you are interested in opening an issue or a pull request, please feel free to do so on [GitHub](https://github.com/pablogila/ATON/).  
For major changes, please get in touch first to discuss the details.  


## Code style

Please try to follow some general guidelines:  
- Use a code style consistent with the rest of the project.  
- Include docstrings to document new additions.  
- Include automated tests for new features or modifications, see [automated testing](#automated-testing).  
- Arrange function arguments by order of relevance. Most implemented functions follow something similar to `function(file, key/s, value/s, optional)`.  


## Automated testing

If you are modifying the source code, you should run the automated tests of the [`ATON/tests/`](https://github.com/pablogila/ATON/tree/main/tests) folder to check that everything works as intended.
To do so, first install PyTest in your environment,
```bash
pip install pytest
```

And then run PyTest inside the `ATON/` directory,
```bash
pytest -vv
```


## Compiling the documentation

The documentation can be compiled automatically to `docs/aton.html` with [Pdoc](https://pdoc.dev/) and ATON itself, by running:
```shell
python3 makedocs.py
```

This runs Pdoc, updating links and pictures, and using the custom theme CSS template from the `css/` folder.


---


# Citation

ATON development started for the following paper, please cite if you use ATON in your work:  
[*Cryst. Growth Des.* 2024, 24, 391−404](https://doi.org/10.1021/acs.cgd.3c01112)  


# License

Copyright (C) 2025 Pablo Gila-Herranz  
This program is free software: you can redistribute it and/or modify
it under the terms of the **GNU Affero General Public License** as published
by the Free Software Foundation, either version **3** of the License, or
(at your option) any later version.  
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the attached GNU Affero General Public License for more details.  

