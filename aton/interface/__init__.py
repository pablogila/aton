"""
# *Ab-initio* interfaces

This module contains interfaces for several *ab-initio* calculation softwares.
These interfaces can be easily expanded with the `aton.text` module.


# Index

| | |  
| --- | --- |  
| `aton.interface.qe`      | Interface for [Quantum ESPRESSO](https://www.quantum-espresso.org/)'s [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) module |  
| `aton.interface.phonopy` | Interface for [Phonopy](https://phonopy.github.io/phonopy/) calculations |  
| `aton.interface.castep`  | Interface for [CASTEP](https://castep-docs.github.io/castep-docs/) calculations |  


# Examples

## Quantum ESPRESSO

To read the output from a Quantum ESPRESSO pw.x calculation,  
```python
from aton.interface import qe
calculation = qe.read_out('relax.out')  # Read to a dictionary
calculation.keys()                       # See the available values
energy = calculation['Energy']           # Final energy from the calculation
```

To modify values from an input file,  
```python
from aton.interface import qe
qe.add_atom('H  0.10  0.20  0.30')         # Add a hydrogen atom to a specific position
qe.set_value('relax.in', 'ecutwfc', 60.0)  # Set the input ecutwfc value
```

Check the full `aton.interface.qe` API reference for more details.


## Phonopy

To perform a phonon calculation from a relaxed structure via Quantum ESPRESSO,  
```python
from aton import interface
# Create the supercell inputs
interface.phonopy.make(dimension='2 2 2', folder='./calculation')
# Sbatch to a cluster
interface.phonopy.sbatch('./calculation')
```

Check the full `aton.interface.phonopy` API reference for more details.


## CASTEP

To read output values from a CASTEP calculation,  
```python
from aton.interface import castep
output = castep.read_castep('calculation.castep')  # Read the output
energy = output['Energy']                          # Get the final energy
```

Check the full `aton.interface.castep` API reference for more details.

"""


from . import qe
from . import phonopy
from . import castep

