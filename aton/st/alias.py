"""
# Description

This module contains common dictionaries to normalise and correct user inputs.
All values are in lowercase to allow comparison with the `string.lower()` method.


# Index

`units`  
`spatial`  
`experiments`  
`files`  
`boolean`  


# Examples

```python
unit = 'Electronvolts'
if unit.lower() in aton.alias.units['eV']:
    ... do stuff ...
```

---
"""


units: dict = {
    'mol'  : ['mol', 'mols', 'mole', 'moles'],
    'g'    : ['g', 'gram', 'grams'],
    'kg'   : ['kg', 'kilogram', 'kilograms'],
    'amu'  : ['amu', 'atomicmassunit', 'atomicmassunits'],
    'eV'   : ['ev', 'electronvolt', 'electronvolts'],
    'meV'  : ['mev', 'millielectronvolt', 'millielectronvolts'],
    'J'    : ['j', 'joule', 'joules'],
    'cal'  : ['cal', 'calorie', 'calories'],
    'kcal' : ['kcal', 'kilocalorie', 'kilocalories'],
    'Ry'   : ['ry', 'rydberg', 'rydbergs'],
    'cm-1' : ['cm^{-1}', 'cm1', 'cm-1', 'cm^-1'],
    'cm'   : ['cm', 'centimeter', 'centimeters'],
    'A'    : ['a', 'aa', 'angstrom', 'angstroms', 'armstrong', 'armstrongs'],
    'bohr' : ['bohr', 'bohrs', 'bohrradii'],
    'm'    : ['m', 'meter', 'meters'],
    'deg'  : ['deg', 'degree', 'degrees'],
    'rad'  : ['rad', 'radian', 'radians'],
    'bar'  : ['bar', 'bars'],
    'kbar' : ['kbar', 'kilobar', 'kilobars'],
    'Pa'   : ['pa', 'pascal', 'pascals'],
    'GPa'  : ['gpa', 'gigapascal', 'gigapascals'],
    's'    : ['s', 'second', 'seconds'],
    'H'    : ['h', 'hour', 'hours'],
}
"""Dict with unit names."""


spatial: dict = {
    'height' : ['height', 'h'],
    'area'   : ['area', 'a'],
    'volume' : ['volume', 'vol'],
    'x'      : ['x', 'horizontal', 'h'],
    'y'      : ['y', 'vertical', 'v'],
    'z'      : ['z'],
}
"""Dict with different spatial parameters."""


experiments: dict = {
    'ins'   : ['ins', 'inelasticneutronscattering', 'inelastic neutron scattering'],
    'atr'   : ['atr', 'ftir', 'attenuatedtotalreflection', 'attenuated total reflection'],
    'raman' : ['raman'],
    'qens'  : ['qens', 'quasielasticneutronscattering', 'quasielastic neutron scattering', 'quasi elastic neutron scattering'],
}
"""Dictionary with the available experiment types."""


files: dict = {
    'file'  : ['file', 'files', 'f', 'filepath', 'file path', 'filename', 'file name'],
    'dir'   : ['dir', 'directory', 'd', 'folder'],
    'error' : ['error', 'errors', 'e', 'err'],
    }
"""Strings related to files."""


boolean: dict = {
    True  : ['yes', 'YES', 'Yes', 'Y', 'y', 'T', 'True', 'TRUE', 't', 'true', True, 'Si', 'SI', 'si', 'S', 's'],
    False : ['no', 'NO', 'No', 'N', 'n', 'F', 'False', 'FALSE', 'f', 'false', False],
}
"""Strings with booleans such as 'yes' / 'no'."""

