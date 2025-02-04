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


# Examples

## Solving quantum rotational systems

To perform a basic calculation of the eigenvalues for a zero potential:

```python
import aton.qrotor as qr
system = qr.System()
system.gridsize = 200000  # Size of the potential grid
system.B = 1  # Rotational inertia
system.potential_name = 'zero'
system.solve()
system.eigenvalues
# [0.0, 1.0, 1.0, 4.0, 4.0, 9.0, 9.0, ...]  # approx values
```

The accuracy of the calculation increases with bigger gridsizes,
but note that the runtime increases exponentially.

The same calculation can be performed for a methyl group,
in a sine potential of amplitude 30 meV:

```python
import aton.qrotor as qr
import numpy as np
system = qr.System()
system.gridsize = 200000  # Size of the potential grid
system.B = qr.B_CH3  # Rotational inertia of a methyl group
system.potential_name = 'sine'
system.potential_constants = [0, 30, np.pi/2]  # Offset, max, phase
system.solve()
# Plot potential and eigenvalues
qr.plot.energies(system)
# Plot the first wavefunctions
qr.plot.wavefunction(system, levels=[0,1,2], square=True)
```


## Rotational potentials from DFT

To calculate a rotational potential via Quantum ESPRESSO,
running an SCF calculation every 10 degrees:

```python
import aton.qrotor as qr
from aton import interface
# Approx crystal positions of the atoms to rotate
atoms = [
    '1.101   1.204   1.307'
    '2.102   2.205   2.308'
    '3.103   3.206   3.309'
]
# Create the input SCF files, saving the filenames to a list
scf_files = qr.rotate.structure_qe('molecule.in', positions=atoms, angle=10, repeat=True)
# Run the calculations
interface.slurm.sbatch(files=scf_files)
```

To load the calculated potential to a QRotor System,
```python
# Create a 'potential.dat' file with the potential as a function of the angle
qr.potential.from_qe()
system = qr.potential.load()
```

Check the API documentation for more details.

"""


from .system import System
from .constants import *
from . import systems
from . import rotate
from . import potential
from . import solve
from . import plot

