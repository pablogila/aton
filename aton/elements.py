'''
# Description

This module contains functions to sort and analyse element data
from the `aton.atoms` megadictionary, which contains the properties of all elements.
It also contains the tools needed to automatically update said megadictionary.

# Index

- `export_atoms()` Used to update and export the `aton.atoms` megadictionary.
- `split_isotope()`
- `allowed_isotopes()`

# References

Atomic `mass` are in atomic mass units (amu), and come from:
Pure Appl. Chem., Vol. 78, No. 11, pp. 2051-2066, 2006.
The following masses are obtained from Wikipedia:
Ac: 227, Np: 237, Pm: 145, Tc: 98

Isotope `mass`, `mass_number` and `abundance` come from:
J. R. de Laeter, J. K. Böhlke, P. De Bièvre, H. Hidaka, H. S. Peiser, K. J. R. Rosman
and P. D. P. Taylor (2003). 'Atomic weights of the elements. Review 2000 (IUPAC Technical Report)'

Total bound scattering `cross_section` $\\sigma_s$ are in barns (1 b = 100 fm$^2$).
From Felix Fernandez-Alonso's book 'Neutron Scattering Fundamentals' (2013).

---
'''


class Element:
    '''Used in the `aton.atoms` megadictionary to store element data.'''
    def __init__(self=None, Z:int=None, symbol:str=None, name:str=None, mass:float=None, cross_section:float=None, isotope:dict=None):
        self.Z: int = Z
        '''Atomic number (Z). Corresponds to the number of protons / electrons.'''
        self.symbol: str = symbol
        '''Standard symbol of the element.'''
        self.name: str = name
        '''Full name.'''
        self.mass: float = mass
        '''Atomic mass, in atomic mass units (amu).'''
        self.cross_section: float = cross_section
        '''Total bound scattering cross section.'''
        self.isotope: dict = isotope
        '''Dictionary containing the different `Isotope` of the element. The keys are the mass number (A).'''


class Isotope:
    '''Used in the `aton.atoms` megadictionary to store isotope data.'''
    def __init__(self, A:int=None, mass:float=None, abundance:float=None, cross_section:float=None):
        self.A: int = A
        '''Mass number (A) of the isotope. Corresponds to the total number of protons + neutrons in the core.'''
        self.mass: float = mass
        '''Atomic mass of the isotope, in atomic mass units (amu).'''
        self.abundance: float = abundance
        '''Relative abundance of the isotope.'''
        self.cross_section: float = cross_section
        '''Total bound scattering cross section of the isotope.'''


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
            "The `atoms` dictionary can be loaded directly as `aton.atoms`.\n"
            "Use example:\n"
            "```python\n"
            "aluminium_cross_section = aton.atoms['Al'].cross_section\n"
            "He4_mass = aton.atoms['H'].isotope[4].mass\n"
            "```\n\n"
            "---\n"
            "'''\n\n"
            "from .element import Element, Isotope\n\n"
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

