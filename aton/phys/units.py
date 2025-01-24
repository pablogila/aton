"""
# Description

This module contains constants and conversion factors from the 
[2022 CODATA](https://doi.org/10.48550/arXiv.2409.03787)
Recommended Values of the Fundamental Physical Constants.


# Index

- [Conversion factors](#conversion-factors)
    - [Energy](#energy)
    - [Distance](#distance)
    - [Mass](#mass)
    - [Pressure](#pressure)
    - [Time](#time)
    - [Temperature](#temperature)
- [Fundamental Physical Constants](#fundamental-physical-constants)
    - [Universal](#universal)
    - [Electromagnetic](#electromagnetic)
    - [Atomic and nuclear](#atomic-and-nuclear)
        - [General](#general)
        - [Electron](#electron)
        - [Proton](#proton)
        - [Neutron](#neutron)
        - [Deuteron](#deuteron)
        - [Alpha particle](#alpha-particle)
    - [Physicochemical](#physicochemical)


# Examples

```python
from aton import phys
energy_in_cm1 = 1000 * phys.meV_to_cm1       # 8065.5
length_in_angstroms = 10.0 * phys.bohr_to_A  # 5.29177210544
phys.hbar   # 1.0545718176461565e-34
```

In general, greek letters from constant names are
[romanized](https://en.wikipedia.org/wiki/Romanization_of_Greek#Ancient_Greek),
excepting $\\mu$ which uses `u`.

---

## Conversion factors

For quick unit conversion, as `value_initial * initial_to_final`

### Energy
Note that `cm1` refers to cm$^{-1}$.
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
### Distance
Note that `A` refers to Angstroms.
"""
A_to_m      = 1.0e-10
m_to_A      = 1.0 / A_to_m
bohr_to_m   = 5.29177210544e-11
m_to_bohr   = 1.0 / bohr_to_m
A_to_bohr   = A_to_m * m_to_bohr
bohr_to_A   = 1.0 / A_to_bohr

"""---
### Mass
"""
amu_to_kg   = 1.66053906660e-27
kg_to_amu   = 1.0 / amu_to_kg
kg_to_g     = 1000.0
g_to_kg     = 1.0 / kg_to_g

"""---
### Pressure
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
### Time
"""
H_to_s      = 3600.0
s_to_H      = 1.0 / H_to_s

"""---
### Temperature
Note that temperature constants must be added, not multiplied.
"""
C_to_K = 273.15
K_to_C = -C_to_K

"""---
## Fundamental Physical Constants
Using SI units unless stated otherwise.

### Universal
"""
c = 299792458
"""$c$ | speed of light in vacuum, in m/s"""
u0 = 1.25663706127e-6
"""$\\mu_0$ | vacuum magnetic permeability, in N·A$^{-2}$ ($4\\pi\\alpha\\hbar/e^2 c$)"""
e0 = 1.25663706127e-6
"""$\\epsilon_0$ | vacuum electric permittivity, in F·m$^{-1}$ ($1/\\mu_0 c^2$)"""
Z0 = 376.730313412
"""$Z_0$ | characteristic impedance of vacuum, in $\\Omega$ ($\\mu_0 c$)"""
G = 6.67430e-11
"""Newtonian constant of gravitation, in m$^3$·kg$^{-1}$·s$^{-1}$"""
h = 6.62607015e-34
"""$h$ | Planck constant, in J·s"""
h_eV = h * J_to_eV
"""$h$ | Planck constant, in eV·s"""
hbar = h / (2 * np.pi)
"""$\\hbar$ | reduced Planck constant, in J·s"""
hbar_eV = h_eV / (2 * np.pi)
"""$\\hbar$ | reduced Planck constant, in eV·s

---
### Electromagnetic
"""
e = 1.602176634e-19
"""$e$ | elementary charge, in C"""
P0 = 2.067833848e-15
"""$\\Phi_0$ | magnetic flux quantum, in Wb ($2\\pi\\hbar/(2e)$)"""
G0 = 7.748091729e-5
"""$G_0$ | conductance quantum, in S ($2e^2/2\\pi h$)"""
KJ = 483597.8484e9
"""$K_J$ | Josephson constant, in Hz·V$^{-1}$ (2e/h)"""
RK = 25812.80745
"""$R_K$ | von Klitzing constant, in $\\Omega$ ($\\mu_0 c/2\\alpha = 2\\pi\\hbar/e^2$)"""
uB = 9.2740100657e-24
"""$\\mu_B$ | Bohr magneton, in J·T$^{-1}$ ($e\\hbar / 2m_e$)""" 
uN = 5.0507837393e-27
"""$\\mu_N$ | nuclear magneton, in J·T$^{-1}$ ($e\\hbar / 2m_p$)

---
### Atomic and nuclear
#### General
"""
a = 7.2973525643e-3
"""$\\alpha$ | fine-structure constant ($e^2 / 4 \\pi \\epsilon_0 \\hbar c$)"""
a1 = 137.035999177
"""$\\alpha^{-1}$ | inverse fine-structure constant"""
cRinf = 3.2898419602500e15 
"""$cR\\infty$ | Rydberg frequency, in Hz ($\\alpha^2m_e c^2/2h = E_h/2h$)"""
Rinf = 10973731.568157
"""$R\\infty$ | Rydberg constant, in $[m^{-1}]^a$"""
a0 = 5.29177210544e-11
"""$a_0$ | Bohr radius, in m"""
Eh = 4.3597447222060e-18
"""$E_h$ | Hartree energy, in J ($\\alpha^2m_ec^2=e^2/4\\pi\\epsilon_0a_0=2h c R_{\\infty}$)

---
#### Electron
"""
me = 9.1093837139-31
"""$m_e$ | electron mass, in kg"""
me_uma = 5.485799090441e-4
"""$m_e$ | electron mass, in uma"""
mec2 = 8.1871057880e-14
"""$m_e c^2$ | electron mass energy equivalent, in J"""
mec2_eV = 510998.95069
"""$m_e c^2$ | electron mass energy equivalent, in eV"""
lC = 2.42631023538e-12
"""$\\lambda_C$ | Compton wavelength, in $[m]^a$"""
re = 2.8179403205e-15
"""$r_e$ | classical electron radius, in m ($\\alpha^2 a_0$)"""
se = 6.6524587051e-29
"""$\\sigma_e$ | Thomson cross section, in m$^2$ ($(8\\pi / 3)r_e^2$)"""
ue = -9.2847646917e-24
"""$\\mu_e$ | electron magnetic moment, in J·T$^{-1}$

---
#### Proton
"""
mp = 1.67262192595-27
"""$m_p$ | proton mass, in kg"""
mp_uma = 1.0072764665789
"""$m_p$ | proton mass, in uma"""
mpc2 = 1.50327761802e-10
"""$m_p c^2$ | proton mass energy equivalent, in J"""
mpc2_eV = 938272089.43
"""$m_p c^2$ | proton mass energy equivalent, in eV"""
mpme = 1836.152673426
"""$m_p/m_e$ | proton-electron mass ratio"""
lCp = 1.32140985360e-15
"""$\\lambda_{C,p}$ | proton Compton wavelength, in $[m]^a$"""
rp = 8.4075e-16
"""$r_p$ | proton rms charge radius, in m"""
up = 1.41060679545e-26
"""$\\mu_p$ | proton magnetic moment, in J·T$^{-1}$

---
#### Neutron
"""
mn = 1.67492750056e-27
"""$m_n$ | neutron mass, in kg"""
mn_uma = 1.00866491606
"""$m_n$ | neutron mass, in uma"""
mnc2 = 1.50534976514e-10
"""$m_n c^2$ | neutron mass energy equivalent, in J"""
mnc2_eV = 939565421.94
"""$m_n c^2$ | neutron mass energy equivalent, in eV"""
lCn = 1.31959090382e-15
"""$\\lambda_{C,n}$ | neutron compton wavelength, in $[m]^a$"""
un = -9.6623653e-27
"""$\\mu_n$ | neutron magnetic moment, in J·T$^{-1}$

---
#### Deuteron
"""
md = 3.3435837768e-27
"""$m_d$ | deuteron mass, in kg"""
md_uma = 2.013553212544
"""$m_d$ | deuteron mass, in uma"""
mdc2 = 3.00506323491e-10
"""$m_d c^2$ | deuteron mass energy equivalent, in J"""
mdc2_eV = 1875612945
"""$m_d c^2$ | deuteron mass energy equivalent, in eV"""
rd = 2.12778e-15
"""$r_d$ | deuteron rms charge radius, in m"""
ud = 4.330735087e-27
"""$\\mu_d$ | deuteron magnetic moment, in J·T$^{-1}$

---
#### Alpha particle
"""
ma = 6.6446573450e-27
"""$m_\\alpha$ | alpha particle mass, in kg"""
mac2 = 5.9719201997e-10
"""$m_\\alpha$ | alpha particle mass energy equivalent, in J"""
mac2_eV = 3727379411.8
"""$m_\\alpha$ | alpha particle mass energy equivalent, in eV"""
ra = 1.6785e-15
"""$r_\\alpha$ | alpha particle rms charge radius, in m

---
### Physicochemical
"""
NA = 6.02214076e23
"""$N_A$ | Avogadro constant, in mol$^{-1}$"""
k = 1.380649e-23
"""$k$ | Boltzmann constant, in J·K$^{-1}$"""
k_eV = 8.617333262e-5
"""$k$ | Boltzmann constant, in eV·K$^{-1}$"""
mu = 1.66053906892e-27
"""$m_u$ | atomic mass constant, in kg ($\\frac{1}{12}m(^{12}C)$)"""
muc2 = 1.49241808768e-10
"""$m_u c^2$ | atomic mass constant energy equivalent, in J"""
muc2_eV = 931494103.72
"""$m_u c^2$ | atomic mass constant energy equivalent, in eV"""
R = 8.314462618
"""$R$ | molar gas constant, in J·mol$^{-1}$K$^{-1}$ ($N_A k$)"""
F = 96485.33212
"""$F$ | Faraday constant, in C·mol$^{-1}$ ($N_A e$)"""
s = 5.670374419e-8
"""$\\sigma$ | Stefan-Boltzmann constant, in W·m$^{-2}$·K$^{-4}$ ($(\\pi^2/60)k^4 /\\hbar^3 c^2$)"""

