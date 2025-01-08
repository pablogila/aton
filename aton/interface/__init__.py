"""
# *Ab-initio* interfaces

This module contains interfaces for several *ab-initio* calculation softwares.

These interfaces can be easily expanded with the `aton.text` module.

## Quantum ESPRESSO

The interface `aton.interface.qe` can read and modify data
from the [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
module of [Quantum ESPRESSO](https://www.quantum-espresso.org/).

## Phonopy

The submodule `aton.interface.phonopy` is used to simplify the
calculation of phonon modes with [Phonopy](https://phonopy.github.io/phonopy/),
using Quantum ESPRESSO as calculator.

## CASTEP

The submodule `aton.interface.castep` is used
to read [CASTEP](https://castep-docs.github.io/castep-docs/) output files.

"""

from . import qe
from . import phonopy
from . import castep

