"""
# Description

This module is used to extract isotope information from text strings.


# Index

| | |
| --- | --- |
| `split_isotope()`    | Splits element name and mass number |
| `allowed_isotopes()` | Returns the available mass numbers for a given element |


# Examples

All functions can be called from the phys subpackage directly, as:
```python
from aton import phys
phys.split_isotope('He4')    # (He, 4)
phys.allowed_isotopes('Li')  # (6, 7)
```

---
"""


from .atoms import atoms as atoms_megadict


def split_isotope(name:str) -> tuple:
    """Split the `name` of an isotope into the element and the mass number, eg. He4 -> He, 4.

    If the isotope is not found in the `aton.atoms` megadictionary it raises an error,
    informing of the allowed mass numbers (A) values for the given element.
    """
    element = ''.join(filter(str.isalpha, name))
    isotope = int(''.join(filter(str.isdigit, name)))
    isotopes = allowed_isotopes(element)
    if not isotope in isotopes:
        raise KeyError(f'Unrecognised isotope: {name}. Allowed mass numbers for {element} are: {isotopes}')
    return element, isotope


def allowed_isotopes(element) -> list:
    """Return a list with the allowed mass numbers (A) of a given `element`.

    These mass numbers are used as isotope keys in the `aton.atoms` megadictionary.
    """
    from .atoms import atoms
    if not element in atoms.keys():
        try:
            element, _ = split_isotope(element)
        except KeyError:
            raise KeyError(f'Unrecognised element: {element}')
    isotopes = atoms[element].isotope.keys()
    return isotopes

