"""
# Description

This function is used to update and export the `aton.phys.atoms` megadictionary.


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
            "It can be loaded directly as `aton.phys.atoms`.\n"
            "It is managed and updated automatically with `aton.phys.functions`.\n\n\n"
            "# Index\n\n"
            "| | |\n"
            "| --- | --- |\n"
            "| `Element` | Used as values in the `atoms` dict, stores element properties |\n"
            "| `Isotope` | Used as values in `Element.isotope`, stores isotope properties |\n"
            "| `atoms`   | The dict with data from all elements |\n\n\n"
            "# Examples\n\n"
            "```python\n"
            "from aton.phys import atoms\n"
            "aluminium_neutron_cross_section = atoms['Al'].cross_section  # 1.503\n"
            "He4_mass = atoms['He'].isotope[4].mass  # 4.0026032497\n\n"
            "```\n\n"
            "---\n"
            "'''\n\n\n"
            "class Element:\n"
            "    '''Used as values in the `aton.phys.atoms` megadictionary to store element data.'''\n"
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
            "    '''Used as values in `Element.isotope` to store isotope data.'''\n"
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

