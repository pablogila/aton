"""
# Description

This module contains useful constants and conversion factors.


# Index

[Energy conversion factors](#energy-conversion-factors)  
[Distance conversion factors](#distance-conversion-factors)  
[Mass conversion factors](#mass-conversion-factors)  
[Pressure conversion factors](#pressure-conversion-factors)  
[Time conversion factors](#time-conversion-factors)  
[Universal constants](#universal-constants)  


# Examples

```python
from aton import phys
energy_in_cm1 = 1000 * phys.meV_to_cm1       # 8065.5
length_in_angstroms = 10.0 * phys.bohr_to_A  # 5.29177210544
phys.hbar   # 1.0545718176461565e-34
```

---

## Energy conversion factors
Note that `cm` refers to cm$^{-1}$.
"""

import numpy as np

eV_to_meV   = 1000.0
meV_to_eV   = 0.001
meV_to_cm1  = 8.0655
cm1_to_meV  = 1.0 / meV_to_cm1
eV_to_J     = 1.602176634e-19
J_to_eV     = 1.0 / eV_to_J
meV_to_J    = meV_to_eV * eV_to_J
J_to_meV    = J_to_eV * eV_to_meV
Ry_to_eV    = 13.605693122990
eV_to_Ry    = 1.0 / Ry_to_eV
Ry_to_J     = 2.1798723611030e-18
J_to_Ry     = 1.0 / Ry_to_J
cal_to_J    = 4.184
J_to_cal    = 1 / cal_to_J
kcal_to_J   = cal_to_J * 1000.0
J_to_kcal   = 1 / kcal_to_J

"""---
## Distance conversion factors
Note that `A` refers to Angstroms.
"""
A_to_m      = 1.0e-10
m_to_A      = 1.0 / A_to_m
bohr_to_m   = 5.29177210544e-11
m_to_bohr   = 1.0 / bohr_to_m
A_to_bohr   = A_to_m * m_to_bohr
bohr_to_A   = 1.0 / A_to_bohr

"""---
## Mass conversion factors
"""
amu_to_kg   = 1.66053906660e-27
kg_to_amu   = 1.0 / amu_to_kg
kg_to_g     = 1000.0
g_to_kg     = 1.0 / kg_to_g

"""---
## Pressure conversion factors
"""
GPa_to_Pa   = 1.0e9
Pa_to_GPa   = 1.0 / GPa_to_Pa
kbar_to_bar = 1000.0
bar_to_kbar = 1.0 / kbar_to_bar
Pa_to_bar   = 1.0e-5
bar_to_Pa   = 1.0 / Pa_to_bar
GPa_to_kbar = GPa_to_Pa * Pa_to_bar * bar_to_kbar
kbar_to_GPa = 1.0 / GPa_to_kbar

"""---
## Time conversion factors
Note that `H` refers to hours.
"""
H_to_s      = 3600.0
s_to_H      = 1.0 / H_to_s

"""---
## Universal constants
Given in SI units unless stated otherwise.
"""
h = 6.62607015e-34      # J s
"""Planck constant, in J·s."""
h_eV = h * J_to_eV
"""Planck constant, in eV·s."""
hbar = h / (2 * np.pi)  # J s
"""Reduced Planck constant, in J·s."""
hbar_eV = h_eV / (2 * np.pi)
"""
Reduced Planck constant, in eV·s.
"""

