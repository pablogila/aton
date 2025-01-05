<p align="center"><img width="50.0%" src="pics/aton.png"></p>

Welcome to the **A**b-ini**T**i**O** and **N**eutron research toolbox, or [Aton](https://en.wikipedia.org/wiki/Aten).
Inspired by its ancient Egyptian deity counterpart, this all-in-one Python package provides powerful and comprehensive tools for cutting-edge materials research, focused on (but not limited to) neutron science.  

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

## Submodules

Aton contains the following modules:  

- [text](https://pablogila.github.io/Aton/aton/text.html). See [General text edition](#general-text-edition).
- [interface](https://pablogila.github.io/Aton/aton/interface.html). See [Interfaces for ab-initio codes](#interfaces-for-ab-initio-codes).  
- [spectra](https://pablogila.github.io/Aton/aton/spectra.html). See [Spectral analysis tools](#spectral-analysis-tools).
- [units](https://pablogila.github.io/Aton/aton/units.html). Physical constants and conversion factors.
- [atoms](https://pablogila.github.io/Aton/aton/atoms.html). Megadictionary with data for all chemical elements.  
- [elements](https://pablogila.github.io/Aton/aton/elements.html). Sort and analyse element data, and manage the atoms dictionary.  
- [file](https://pablogila.github.io/Aton/aton/file.html). Manipulate files.  
- [call](https://pablogila.github.io/Aton/aton/call.html). Run bash scripts and related.  
- [alias](https://pablogila.github.io/Aton/aton/alias.html). Useful dictionaries for user input correction.  

## General text edition

The [text](https://pablogila.github.io/Aton/aton/text.html) module includes the following general text-related submodules:

- [text.find](https://pablogila.github.io/Aton/aton/text/find.html). Search for specific content in a text file.  
- [text.edit](https://pablogila.github.io/Aton/aton/text/edit.html). Manipulate text files.  
- [text.extract](https://pablogila.github.io/Aton/aton/text/extract.html). Extract data from raw text strings.  

## Interfaces for ab-initio codes

The [interface](https://pablogila.github.io/Aton/aton/interface.html) module contains interfaces for several *ab-initio* codes. These are powered by the [text](https://pablogila.github.io/Aton/aton/text.html) module and can be easily extended. The following interfaces are included:  

- [interface.qe](https://pablogila.github.io/Aton/aton/interface/qe.html). Interface for [Quantum ESPRESSO](https://www.quantum-espresso.org/) calculations.
- [interface.phonopy](https://pablogila.github.io/Aton/aton/interface/phonopy.html). Interface for [Phonopy](https://phonopy.github.io/phonopy/) calculations.
- [interface.castep](https://pablogila.github.io/Aton/aton/interface/castep.html) Interface for [CASTEP](https://castep-docs.github.io/castep-docs/) calculations.

## Spectral analysis tools

The [spectra](https://pablogila.github.io/Aton/aton/spectra.html) module IS YET TO BE IMPLEMENTED.
- Things...

---

# Contributing

If you are interested in opening an issue or a pull request, please feel free to do so on [GitHub](https://github.com/pablogila/Aton/).  
For major changes, please get in touch first to discuss the details.  

## Code style

Please try to follow some general guidelines:  
- Use a code style consistent with the rest of the project.  
- Include docstrings to document new additions.  
- Include tests for new features or modifications.  
- Arrange function arguments by order of relevance. Most implemented functions follow something similar to `function(file, key/s, value/s, optional)`.  

## Testing with PyTest

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

The documentation can be compiled automatically to `docs/aton.html` with [pdoc](https://pdoc.dev/) and Aton itself, by running:
```shell
python3 makedocs.py
```

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

