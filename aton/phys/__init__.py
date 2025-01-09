"""
# Physico-chemical constants

This subpackage contains:
- `units`
- `atoms`
- `elements`


Use example:

```python
from aton import phys
phys.eV_to_J  # 1.602176634e-19
phys.atoms['H'].isotope[2].mass  # 2.0141017779
```

# References

## `aton.units`

These values come from the 2022 CODATA Internationally
recommended 2022 values of the Fundamental Physical Constants.

## `aton.atoms`

Atomic `mass` are in atomic mass units (amu), and come from:
Pure Appl. Chem., Vol. 78, No. 11, pp. 2051-2066, 2006.
The following masses are obtained from Wikipedia:
Ac: 227, Np: 237, Pm: 145, Tc: 98

Isotope `mass`, `mass_number` and `abundance` come from:
J. R. de Laeter, J. K. Böhlke, P. De Bièvre, H. Hidaka, H. S. Peiser, K. J. R. Rosman
and P. D. P. Taylor (2003). 'Atomic weights of the elements. Review 2000 (IUPAC Technical Report)'

Total bound scattering `cross_section` $\\sigma_s$ are in barns (1 b = 100 fm$^2$).
From Felix Fernandez-Alonso's book 'Neutron Scattering Fundamentals' (2013).

"""

from .units import *
from .functions import *
from .atoms import atoms

