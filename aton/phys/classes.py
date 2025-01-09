"""
The `aton.phys.atoms` megadictionary contains the `Element` and `Isotope` classes defined in this submodule.
"""


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

