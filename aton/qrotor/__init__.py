"""
# QRotor
 
The QRotor module is used to study the energy levels of quantum rotations, such as methyl and amine groups.

This module uses meV as default units in the calculations.


# Index

| | |
| --- | --- |
| `aton.qrotor.rotate`    | Rotate specific atoms from structural files |
| `aton.qrotor.constants` | Bond lengths and inertias |
| `aton.qrotor.system`    | Definition of the quantum `System` object |
| `aton.qrotor.systems`   | Functions to manage several System objects |
| `aton.qrotor.potential` | Potential definitions and loading functions |
| `aton.qrotor.solve`     | Solve rotation eigenvalues and eigenvectors |
| `aton.qrotor.plot`      | Plotting functions |

"""


from .system import System
from .constants import *
from . import systems
from . import rotate
from . import potential
from . import solve
from . import plot

