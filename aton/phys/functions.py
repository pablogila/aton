"""
# Description

This module contains functions to sort and analyse
chemical data using the `aton.phys.atoms` megadictionary,
which contains the properties of all elements.
It also contains the tools needed to
automatically update said megadictionary.


# Index

| | |
| --- | --- |
| `export_atoms()`     | Used to update and export the `aton.phys.atoms` dict |
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


def export_atoms(
        atoms:dict=atoms_megadict,
        filename='exported_atoms.py'
    ) -> None:
    """Export a dictionary of chemical elements to a python file.

    This is used to build and update the `aton.atoms` megadictionary, that contains
    all the element data, such as masses, cross-sections, etc.
    The `atoms.py` file must be modified here.
    """
    with open(filename, 'w') as f:
        # Write the docstrings
        f.write(
            "'''\n"
            "# Description\n\n"
            "This module contains the `atoms` megadictionary,\n"
            "which contains the properties of all elements.\n"
            "It is managed and updated automatically with `aton.phys.functions`.\n\n\n"
            "# Index\n\n"
            "| | |\n"
            "| --- | --- |\n"
            "| `Element` | Used as values in the `atoms` dict, stores element properties |\n"
            "| `Isotope` | Used as values in `Element.isotope`, stores isotope properties |\n"
            "| `atoms`   | The dict with data from all elements |\n\n\n"
            "# Examples\n\n"
            "The `atoms` dictionary can be loaded directly as `aton.phys.atoms`, as shown below:\n"
            "```python\n"
            "from aton import phys\n"
            "aluminium_neutron_cross_section = phys.atoms['Al'].cross_section  # 1.503\n"
            "He4_mass = phys.atoms['He'].isotope[4].mass  # 4.0026032497\n\n"
            "```\n\n"
            "---\n"
            "'''\n\n\n"
            "class Element:\n"
            "    '''Used in the `aton.atoms` megadictionary to store element data.'''\n"
            "    def __init__(self=None, Z:int=None, symbol:str=None, name:str=None, mass:float=None, cross_section:float=None, isotope:dict=None):\n"
            "        self.Z: int = Z\n"
            "        '''Atomic number (Z). Corresponds to the number of protons / electrons.'''\n"
            "        self.symbol: str = symbol\n"
            "        '''Standard symbol of the element.'''\n"
            "        self.name: str = name\n"
            "        '''Full name.'''\n"
            "        self.mass: float = mass\n"
            "        '''Atomic mass, in atomic mass units (amu).'''\n"
            "        self.cross_section: float = cross_section\n"
            "        '''Total bound scattering cross section.'''\n"
            "        self.isotope: dict = isotope\n"
            "        '''Dictionary containing the different `Isotope` of the element.\n"
            "        The keys are the mass number (A).\n"
            "        '''\n\n\n"
            "class Isotope:\n"
            "    '''Used in the `aton.atoms` megadictionary to store isotope data.'''\n"
            "    def __init__(self, A:int=None, mass:float=None, abundance:float=None, cross_section:float=None):\n"
            "        self.A: int = A\n"
            "        '''Mass number (A) of the isotope.\n"
            "        Corresponds to the total number of protons + neutrons in the core.\n"
            "        '''\n"
            "        self.mass: float = mass\n"
            "        '''Atomic mass of the isotope, in atomic mass units (amu).'''\n"
            "        self.abundance: float = abundance\n"
            "        '''Relative abundance of the isotope.'''\n"
            "        self.cross_section: float = cross_section\n"
            "        '''Total bound scattering cross section of the isotope.'''\n\n\n"
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
                    f.write(f"            {iso.A} : Isotope(\n")
                    if iso.A:
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

