"""
# Physico-chemical constants

This subpackage contains universal physical constants,
as well as chemical data from all known elements.
It also includes functions to manage this data.


# Index

| | |
| --- | --- |
| `aton.phys.units`     | Universal constants and conversion factors |
| `aton.phys.atoms`     | Data from all chemical elements |
| `aton.phys.functions` | Functions to sort and manage element data from the `aton.phys.atoms` dict |


# Examples

All values and functions from **phys** submodules can be
loaded directly as `phys.value` or `phys.function()`,
as in the example below.

```python
from aton import phys
phys.eV_to_J                     # 1.602176634e-19
phys.atoms['H'].isotope[2].mass  # 2.0141017779
phys.split_isotope('He4')        # ('He', 4)
```

See the API reference of the specific modules for more information.


# References

## `aton.phys.units`

Constant values come from the [2022 CODATA](https://doi.org/10.48550/arXiv.2409.03787) Recommended Values of the Fundamental Physical Constants.

Conversion factors for neutron scattering come from
[David L. Price and Felix Fernandez-Alonso, *Neutron Scattering Fundamentals*, Experimental methods in the physical sciences, Elsevier Academic Press (2013)](https://doi.org/10.1016/B978-0-12-398374-9.00001-2),
and from
[M. Bée, "Quasielastic Neutron scattering", Adam Hilger, Bristol and Philadelphia (1988)](https://www.ncnr.nist.gov/instruments/dcs/dcs_usersguide/Conversion_Factors.pdf);


## `aton.phys.atoms`

Atomic `mass` are in atomic mass units (amu), and come from:
[M. E. Wieser, *Atomic weights of the elements 2005*, Pure and Applied Chemistry 78, 2051–2066 (2006)](https://doi.org/10.1351/pac200678112051).
The following masses are obtained from Wikipedia:
Ac: 227, Np: 237, Pm: 145, Tc: 98.

Isotope `mass`, `mass_number` and `abundance` come from
[J. R. de Laeter *et al*., *Atomic weights of the elements 2000*, Pure and Applied Chemistry 75, 683–800 (2003)](https://doi.org/10.1351/pac200375060683).

Total bound scattering `cross_sections` $\\sigma_s$ are in barns (1 b = 100 fm$^2$ = 10e-28 m$^2$). From
[David L. Price and Felix Fernandez-Alonso, *Neutron Scattering Fundamentals*, Experimental methods in the physical sciences, Elsevier Academic Press (2013)](https://doi.org/10.1016/B978-0-12-398374-9.00001-2).

"""

from .units import *
from .functions import *
from .atoms import atoms

