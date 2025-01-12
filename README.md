<p align="center"><img width="40.0%" src="pics/aton.png"></p>


# Welcome to Aton

The **A**b-ini**T**i**O** & **N**eutron research toolbox,
or [Aton](https://pablogila.github.io/Aton/),
provides powerful and comprehensive tools
for cutting-edge materials research,
focused on (but not limited to) neutron science.

Just like its [ancient Egyptian deity](https://en.wikipedia.org/wiki/Aten) counterpart,
this all-in-one Python package contains a range of tools from spectra normalisation to deuteration estimations.
A set of physico-chemical constants and definitions is also included.
Aton also allows you to easily create, edit and analyse all kinds of text files,
with a special focus on *ab-initio* calculation files.
In particular, it contains interfaces for [Quantum ESPRESSO](https://www.quantum-espresso.org/),
[Phonopy](https://phonopy.github.io/phonopy/) and [CASTEP](https://castep-docs.github.io/castep-docs/).  

The source code is available on [GitHub](https://github.com/pablogila/Aton/).   
Check the [full documentation online](https://pablogila.github.io/Aton/).  


---


# Installation

As always, it is recommended to install your packages in a virtual environment:  
```bash
python3 -m venv .venv
source .venv/bin/activate
```


## With pip

The fastest way to install Aton is through pip:  
```bash
pip install aton
```


## From source

Optionally, you can install Aton from the [GitHub repository](https://github.com/pablogila/Aton/).  

First install the dependencies:  
```bash
pip install pandas numpy scipy matplotlib
```

Then clone the repository or download the [latest stable release](https://github.com/pablogila/Aton/tags) as a ZIP, unzip it, and run inside the `Aton/` directory:  
```bash
pip install .
```


---


# Documentation

The full Aton documentation is available [online](https://pablogila.github.io/Aton/).  
An offline version of the documentation is found at `docs/aton.html`.  
Code examples are included in the [`Aton/examples/`](https://github.com/pablogila/Aton/tree/main/examples) folder.    


## Interfaces for ab-initio codes

The **interface** module contains interfaces for several *ab-initio* codes.
These are powered by the `aton.text` module and can be easily extended.

### [aton.interface](https://pablogila.github.io/Aton/aton/interface.html)

| | |  
| --- | --- |  
| [interface.qe](https://pablogila.github.io/Aton/aton/interface/qe.html)           | Interface for [Quantum ESPRESSO](https://www.quantum-espresso.org/)'s [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) module |  
| [interface.phonopy](https://pablogila.github.io/Aton/aton/interface/phonopy.html) | Interface for [Phonopy](https://phonopy.github.io/phonopy/) calculations |  
| [interface.castep](https://pablogila.github.io/Aton/aton/interface/castep.html)   | Interface for [CASTEP](https://castep-docs.github.io/castep-docs/) calculations |  


## Physico-chemical constants

The **phys** module contains physico-chemical definitions.
Values are accessed directly as `phys.value` or `phys.function()`.  

### [aton.phys](https://pablogila.github.io/Aton/aton/phys.html)

| | |  
| --- | --- |  
| [phys.units](https://pablogila.github.io/Aton/aton/phys/units.html)         | Physical constants and conversion factors |  
| [phys.atoms](https://pablogila.github.io/Aton/aton/phys/atoms.html)         | Megadictionary with data for all chemical elements |  
| [phys.functions](https://pablogila.github.io/Aton/aton/phys/functions.html) | Functions to sort and analyse element data, and to update the atoms dictionary |  


## Spectra analysis

The **spx** module includes tools for spectral analysis from
Inelastic Neutron Scattering, Raman, Infrared, etc.  

### [aton.spx](https://pablogila.github.io/Aton/aton/spx.html)

| | |  
| --- | --- |  
| [spx.classes](https://pablogila.github.io/Aton/aton/spx/classes.html)     | Class definitions for the spectra module |  
| [spx.fit](https://pablogila.github.io/Aton/aton/spx/fit.html)             | Spectra fitting functions |  
| [spx.normalize](https://pablogila.github.io/Aton/aton/spx/normalize.html) | Spectra normalization |  
| [spx.plot](https://pablogila.github.io/Aton/aton/spx/plot.html)           | Plotting |  
| [spx.deuterium](https://pablogila.github.io/Aton/aton/spx/deuterium.html) | Deuteration estimations via INS |  
| [spx.samples](https://pablogila.github.io/Aton/aton/spx/samples.html)     | Sample materials for testing |  


## General text edition

The **text** module includes tools for general text edition.  

### [aton.text](https://pablogila.github.io/Aton/aton/text.html)

| | |  
| --- | --- |  
| [text.find](https://pablogila.github.io/Aton/aton/text/find.html)       | Search for specific content in text files |  
| [text.edit](https://pablogila.github.io/Aton/aton/text/edit.html)       | Manipulate text files |  
| [text.extract](https://pablogila.github.io/Aton/aton/text/extract.html) | Extract data from raw text strings |  


## System tools

The **st** module contains System Tools for common tasks across subpackages.  

### [aton.st](https://pablogila.github.io/Aton/aton/st.html)

| | |  
| --- | --- |  
| [st.file](https://pablogila.github.io/Aton/aton/st/file.html)   | File manipulation |  
| [st.call](https://pablogila.github.io/Aton/aton/st/call.html)   | Run bash scripts and related |  
| [st.alias](https://pablogila.github.io/Aton/aton/st/alias.html) | Useful dictionaries for user input correction |  


---


# Contributing

If you are interested in opening an issue or a pull request, please feel free to do so on [GitHub](https://github.com/pablogila/Aton/).  
For major changes, please get in touch first to discuss the details.  


## Code style

Please try to follow some general guidelines:  
- Use a code style consistent with the rest of the project.  
- Include docstrings to document new additions.  
- Include automated tests for new features or modifications, see [automated testing](#automated-testing).  
- Arrange function arguments by order of relevance. Most implemented functions follow something similar to `function(file, key/s, value/s, optional)`.  


## Automated testing

If you are modifying the source code, you should run the automated tests of the [`Aton/tests/`](https://github.com/pablogila/Aton/tree/main/tests) folder to check that everything works as intended.
To do so, first install PyTest in your environment,
```bash
pip install pytest
```

And then run PyTest inside the `Aton/` directory,
```bash
pytest -vv
```


## Compiling the documentation

The documentation can be compiled automatically to `docs/aton.html` with [Pdoc](https://pdoc.dev/) and Aton itself, by running:
```shell
python3 makedocs.py
```

This runs Pdoc, updating links and pictures, and using the custom theme CSS template from the `css/` folder.


---


# License

Copyright (C) 2024  Pablo Gila-Herranz  
This program is free software: you can redistribute it and/or modify
it under the terms of the **GNU Affero General Public License** as published
by the Free Software Foundation, either version **3** of the License, or
(at your option) any later version.  
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the attached GNU Affero General Public License for more details.  

