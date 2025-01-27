"""
# QRotor
 
The QRotor module is used to study the energy levels of quantum rotations, such as methyl and amine groups.

This module uses meV as default units in the calculations.


# Index

| | |
| --- | --- |
| `aton.qrotor.classes`   | Definition of the `QSys` and `QExp` classes |
| `aton.qrotor.constants` | Bond lengths and inertias |
| `aton.qrotor.rotate`    | Rotate specific atoms from structural files |
| `aton.qrotor.potential` | Potential definitions and loading functions |
| `aton.qrotor.solve`     | Solve rotation eigenvalues and eigenvectors |
| `aton.qrotor.plot`      | Plotting functions |

"""


from .classes import QSys, QExp
from .constants import *
from . import rotate
from . import potential
from . import solve
from . import plot        ###### TODO: update

