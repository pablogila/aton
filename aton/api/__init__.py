"""
# API interfaces for *ab-initio* codes

This module contains interfaces for several *ab-initio* calculation softwares.
These interfaces can be easily expanded with the `aton.txt` module.


# Index

| | |  
| --- | --- |  
| `aton.api.pwx`     | Interface for [Quantum ESPRESSO](https://www.quantum-espresso.org/)'s [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) module |  
| `aton.api.phonopy` | Interface for [Phonopy](https://phonopy.github.io/phonopy/) calculations |  
| `aton.api.castep`  | Interface for [CASTEP](https://castep-docs.github.io/castep-docs/) calculations |  
| `aton.api.slurm`   | Batch jobs via [Slurm](https://slurm.schedmd.com/) |


# Examples

## Quantum ESPRESSO

To read the output from a Quantum ESPRESSO pw.x calculation,  
```python
from aton.api import pwx
# Read to a dictionary
calculation = pwx.read_out('relax.out')
calculation.keys()  # See the available values
# Final energy from the calculation
energy = calculation['Energy']
```

To modify values from an input file,  
```python
from aton.api import pwx
# Add a hydrogen atom to a specific position
pwx.add_atom('relax.in', 'H  0.10  0.20  0.30')
# Set the input ecutwfc value
pwx.set_value('relax.in', 'ecutwfc', 60.0)
```

Check the full `aton.api.pwx` API reference for more details.


## Phonopy

To perform a phonon calculation from a relaxed structure via Quantum ESPRESSO,  
```python
from aton import api
# Create the supercell inputs
api.phonopy.make_supercells(dimension='2 2 2')
# Sbatch to a cluster
api.slurm.sbatch('supercell-', 'template.slurm')
```

Check the full `aton.api.phonopy` API reference for more details.


## CASTEP

To read output values from a CASTEP calculation,  
```python
from aton.api import castep
# Read the output
output = castep.read_castep('calculation.castep')
# Get the final energy
energy = output['Energy']
```

Check the full `aton.api.castep` API reference for more details.

"""


from . import pwx
from . import phonopy
from . import castep
from . import slurm

