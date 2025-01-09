<p align="center"><img width="40.0%" src="pics/aton.png"></p>

Welcome to the **A**b-ini**T**i**O** and **N**eutron research toolbox, or [Aton](https://github.com/pablogila/Aton/).
Just like its ancient Egyptian [deity](https://en.wikipedia.org/wiki/Aten) counterpart, this all-in-one Python package provides powerful and comprehensive tools for cutting-edge materials research, focused on (but not limited to) neutron science.  

Aton provides a range of spectral analysis tools, from spectra normalisation to deuteration estimation using the DINS impulse approximation.  
A set of physico-chemical constants and definitions is also included.  

Aton also allows you to easily create, edit and analyse all kinds of text files, with a special focus on *ab-initio* calculations.
In particular, it contains interfaces for [Quantum ESPRESSO](https://www.quantum-espresso.org/), [Phonopy](https://phonopy.github.io/phonopy/) and [CASTEP](https://castep-docs.github.io/castep-docs/).  

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
pip install pandas numpy scipy
```

Then clone the repository or download the [latest stable release](https://github.com/pablogila/Aton/tags) as a ZIP, unzip it, and run inside the `Aton/` directory:  
```bash
pip install .
```

---

# Documentation

The full Aton documentation is available [online](https://pablogila.github.io/Aton/).  
An offline version of the documentation is found at `docs/aton.html`.  
Code examples are included in the `examples/` folder.    

## Physico-chemical constants

### [phys](https://pablogila.github.io/Aton/aton/phys.html)

| | |
| --- | --- |
| [phys.units](https://pablogila.github.io/Aton/aton/phys/units.html) | Physical constants and conversion factors |
| [phys.atoms](https://pablogila.github.io/Aton/aton/phys/atoms.html) | Megadictionary with data for all chemical elements |  
| [phys.functions](https://pablogila.github.io/Aton/aton/phys/functions.html) | Functions to sort and analyse element data, and to update the atoms dictionary |  

The [phys](https://pablogila.github.io/Aton/aton/phys.html) module contains physico-chemical definitions. All values can be accessed directly as `phys.value` or `phys.function()`.

## Interfaces for ab-initio codes

### [interface](https://pablogila.github.io/Aton/aton/interface.html)

| | |
| --- | --- |
| [interface.qe](https://pablogila.github.io/Aton/aton/interface/qe.html) | Interface for [Quantum ESPRESSO](https://www.quantum-espresso.org/)'s [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) module |  
| [interface.phonopy](https://pablogila.github.io/Aton/aton/interface/phonopy.html) | Interface for [Phonopy](https://phonopy.github.io/phonopy/) calculations |  
| [interface.castep](https://pablogila.github.io/Aton/aton/interface/castep.html) | Interface for [CASTEP](https://castep-docs.github.io/castep-docs/) calculations |  

The [interface](https://pablogila.github.io/Aton/aton/interface.html) module contains interfaces for several *ab-initio* codes. These are powered by the [text](https://pablogila.github.io/Aton/aton/text.html) module and can be easily extended.  

## Spectral analysis tools

> ⚠️ **WARNING:** The spectra module is not yet 100% ported, bugs are expected!

### [spectra](https://pablogila.github.io/Aton/aton/spectra.html)

| | |
| --- | --- |
| [spectra.classes](https://pablogila.github.io/Aton/aton/spectra/classes.html) | Class definitions for the spectra module |
| [spectra.fit](https://pablogila.github.io/Aton/aton/spectra/fit.html) | Spectra fitting functions |
| [spectra.normalize](https://pablogila.github.io/Aton/aton/spectra/normalize.html) | Spectra normalization |
| [spectra.plot](https://pablogila.github.io/Aton/aton/spectra/plot.html) | Plotting |
| [spectra.deuterium](https://pablogila.github.io/Aton/aton/spectra/deuterium.html) | Deuteration estimations via INS |
| [spectra.samples](https://pablogila.github.io/Aton/aton/spectra/samples.html) | Sample materials for testing |

The [spectra](https://pablogila.github.io/Aton/aton/spectra.html) module includes tools to analyse spectral data, such as Inelastic Neutron Scattering, Raman, Infrared, etc.

## General text edition
### [text](https://pablogila.github.io/Aton/aton/text.html)
| | |
| --- | --- |
| [text.find](https://pablogila.github.io/Aton/aton/text/find.html) | Search for specific content in a text file.  | 
| [text.edit](https://pablogila.github.io/Aton/aton/text/edit.html) | Manipulate text files.  |
| [text.extract](https://pablogila.github.io/Aton/aton/text/extract.html) | Extract data from raw text strings.  |

The [text](https://pablogila.github.io/Aton/aton/text.html) module includes tools for general text edition.

## System tools

### [st](https://pablogila.github.io/Aton/aton/st.html)

| | |
| --- | --- |
| [st.file](https://pablogila.github.io/Aton/aton/st/file.html) | Manipulate files |  
| [st.call](https://pablogila.github.io/Aton/aton/st/call.html) | Run bash scripts and related |  
| [st.alias](https://pablogila.github.io/Aton/aton/st/alias.html) | Useful dictionaries for user input correction |  

The [st](https://pablogila.github.io/Aton/aton/st.html) module contains System Tools for common tasks across subpackages.  

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

If you are modifying the source code, you should run the automated tests of the `tests/` folder to check that everything works as intended.
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

This runs Pdoc, updating links and pictures, and using the dark theme CSS template from the `css/` folder.

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

