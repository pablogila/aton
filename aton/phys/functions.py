'''
# Description

This module contains functions to sort and analyse
chemical data using the `aton.phys.atoms` megadictionary,
which contains the properties of all elements.
It also contains the tools needed to
automatically update said megadictionary.

All functions can be called from the phys subpackage directly, as:
```python
from aton import phys
phys.split_isotope('He4')    # He, 4
phys.allowed_isotopes('Li')  # 6, 7
```

# Index

- `export_atoms()`. Used to update and export the `aton.phys.atoms` megadictionary.
- `split_isotope()`
- `allowed_isotopes()`

---
'''


def export_atoms(
        atoms:dict,
        filename='exported_atoms.py'
    ) -> None:
    '''Export a dictionary of chemical elements to a python file.

    This is used to build and update the `aton.atoms` megadictionary, that contains
    all the element data, such as masses, cross-sections, etc.
    '''
    with open(filename, 'w') as f:
        # Write the docstrings
        f.write(
            "'''\n"
            "# Description\n"
            "This module contains the `atoms` megadictionary,\n"
            "which contains the properties of all elements.\n"
            "It is managed and updated automatically with `aton.elements`,\n"
            "which also contains the definition of the dictionary,\n"
            "as well as the literature references for this data.\n\n"
            "The `atoms` dictionary can be loaded directly as `aton.phys.atoms`.\n"
            "Use example:\n"
            "```python\n"
            "from aton import phys\n"
            "aluminium_cross_section = phys.atoms['Al'].cross_section\n"
            "He4_mass = phys.atoms['H'].isotope[4].mass\n"
            "```\n\n"
            "---\n"
            "'''\n\n"
            "from .classes import Element, Isotope\n\n"
        )
        # Start the atom megadictionary
        f.write("atoms = {\n")
        for key, element in atoms.items():
            f.write(f"    '{element.symbol}': Element(\n"
                    f"        Z             = {element.Z},\n"
                    f"        symbol        = '{element.symbol}',\n"
                    f"        name          = '{element.name}',\n")
            if element.mass:
                f.write(f"        mass          = {element.mass},\n")
            if element.cross_section:
                f.write(f"        cross_section = {element.cross_section},\n")
            if element.isotope:
                f.write("        isotope       = {\n")
                for iso in element.isotope.values():
                    f.write(f"            {iso.mass_number} : Isotope(\n")
                    if iso.mass_number:
                        f.write(f"                A             = {iso.A},\n")
                    if iso.mass:
                        f.write(f"                mass          = {iso.mass},\n")
                    if iso.abundance:
                        f.write(f"                abundance     = {iso.abundance},\n")
                    if iso.cross_section:
                        f.write(f"                cross_section = {iso.cross_section},\n")
                    f.write(f"                ),\n")
                f.write("            },\n")
            f.write(f"        ),\n")
        f.write("}\n")
        print(f'Exported elements to {filename}')
    return None


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
    '''Return a list with the allowed mass numbers (A) of a given `element`.

    These mass numbers are used as isotope keys in the `aton.atoms` megadictionary.
    '''
    from .atoms import atoms
    if not element in atoms.keys():
        try:
            element, _ = split_isotope(element)
        except KeyError:
            raise KeyError(f'Unrecognised element: {element}')
    isotopes = atoms[element].isotope.keys()
    return isotopes

