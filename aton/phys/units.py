"""
# Description

This module contains the constants from the 
[2022 CODATA](https://doi.org/10.48550/arXiv.2409.03787)
Recommended Values of the Fundamental Physical Constants.

It also contains useful conversion factors for neutron scattering, from
[David L. Price and Felix Fernandez-Alonso, *Neutron Scattering Fundamentals*, Experimental methods in the physical sciences, Elsevier Academic Press (2013)](https://doi.org/10.1016/B978-0-12-398374-9.00001-2),
and from
[M. Bée, "Quasielastic Neutron scattering", Adam Hilger, Bristol and Philadelphia (1988)](https://www.ncnr.nist.gov/instruments/dcs/dcs_usersguide/Conversion_Factors.pdf);


# Index

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
- [Conversion factors](#conversion-factors)
    - [Energy E](#energy)
    - [Distance](#distance)
    - [Mass](#mass)
    - [Pressure](#pressure)
    - [Time](#time)
    - [Wavelength l](#wavelength)
    - [Wavevector *k*](#wavevector)
    - [Velocity v](#velocity)
    - [Temperature T](#temperature)
    - [Temperature scales](#temperature-scales)
    - [Frequency *v*](#frequency)
    - [Angular frequency *w*](#angular-frequency)
    - [Wavenumber *v*/c](#wavenumber)


# Examples

Units and constants are named as their standard symbol, removing any `/` divider in between.
Inverse of a unit or constant X, as in 1/X or X$^{-1}$, is expressed as `X1`.

Universal constant names contain
[romanized greek letters](https://en.wikipedia.org/wiki/Romanization_of_Greek#Ancient_Greek),
except for $\\mu$ which is used as `u`.

Some examples:  
```python
from aton import phys
# Constants
phys.h     # Planck constant
phys.hbar  # reduced Planck constant
phys.a     # fine-structure constant (alpha)
phys.ue    # electron magnetic moment (mu e)
phys.mn    # neutron mass
phys.mnc2  # neutron mass energy equivalent
# Conversions
# meV to 1/cm
energy_in_cm1 = energy_in_meV * phys.meV_to_cm1
# Bohr to Angstroms
distance_in_angstroms = distance_in_bohr * phys.bohr_to_AA
# m/s to rad/s  (used in neutron scattering)
velocity_in_rads = velocity_in_ms * phys.ms_to_rads
```


---
# Fundamental Physical Constants
Using SI units unless stated otherwise.

## Universal
"""

import numpy as np

c = 299792458
"""$c$ | speed of light in vacuum / natural unit of velocity, in m/s"""
u0 = 1.25663706127e-6
"""$\\mu_0$ | vacuum magnetic permeability, in N·A$^{-2}$ ($4\\pi\\alpha\\hbar/e^2 c$)"""
e0 = 1.25663706127e-6
"""$\\epsilon_0$ | vacuum electric permittivity, in F·m$^{-1}$ ($1/\\mu_0 c^2$)"""
Z0 = 376.730313412
"""$Z_0$ | characteristic impedance of vacuum, in $\\Omega$ ($\\mu_0 c$)"""
G = 6.67430e-11
"""$G$ | Newtonian constant of gravitation, in m$^3$·kg$^{-1}$·s$^{-1}$"""
h = 6.62607015e-34
"""$h$ | Planck constant, in J·s"""
h_eV = 4.135667696923859e-15
"""$h$ | Planck constant, in eV·s"""
hbar = h / (2 * np.pi)
"""$\\hbar$ | reduced Planck constant / natural unit of action, in J·s"""
hbar_eV = h_eV / (2 * np.pi)
"""$\\hbar$ | reduced Planck constant, in eV·s

---
## Electromagnetic
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
## Atomic and nuclear
### General
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
### Electron
"""
me = 9.1093837139-31
"""$m_e$ | electron mass / natural unit of mass, in kg"""
me_uma = 5.485799090441e-4
"""$m_e$ | electron mass, in uma"""
mec2 = 8.1871057880e-14
"""$m_e c^2$ | electron mass energy equivalent / natural unit of energy, in J"""
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
### Proton
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
### Neutron
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
### Deuteron
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
### Alpha particle
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
## Physicochemical
"""
NA = 6.02214076e23
"""$N_A$ | Avogadro constant, in mol$^{-1}$"""
k = 1.380649e-23
"""$k$ | Boltzmann constant, in J·K$^{-1}$"""
k_eV = 8.617333262e-5
"""$k$ | Boltzmann constant, in eV·K$^{-1}$"""
mu = 1.66053906892e-27
"""$m_u$ | atomic mass constant / unified atomic mass unit, in kg ($\\frac{1}{12}m(^{12}C)$)"""
muc2 = 1.49241808768e-10
"""$m_u c^2$ | atomic mass constant energy equivalent, in J"""
muc2_eV = 931494103.72
"""$m_u c^2$ | atomic mass constant energy equivalent, in eV"""
R = 8.314462618
"""$R$ | molar gas constant, in J·mol$^{-1}$K$^{-1}$ ($N_A k$)"""
F = 96485.33212
"""$F$ | Faraday constant, in C·mol$^{-1}$ ($N_A e$)"""
s = 5.670374419e-8
"""$\\sigma$ | Stefan-Boltzmann constant, in W·m$^{-2}$·K$^{-4}$ ($(\\pi^2/60)k^4 /\\hbar^3 c^2$)

---
# Conversion factors

## Energy
"""
Ry_to_eV      = 13.605693122990
Ry_to_meV     = Ry_to_eV * 1000.0
Ry_to_J       = 2.1798723611030e-18

eV_to_Ry      = 1.0 / Ry_to_eV
eV_to_J       = 1.602176634e-19
eV_to_meV     = 1000.0

meV_to_eV     = 1e-3
meV_to_Ry     = 1.0 / Ry_to_meV
meV_to_J      = 1.602176634e-22
meV_to_AA     = 9.045
meV_to_AA1    = 0.6947
meV_to_ms     = 437.4 
meV_to_K      = 11.604
meV_to_THz    = 0.2418
meV_to_rads   = 1.519e12
meV_to_cm1    = 8.0655
meV_to_kJmol  = 0.0965

cal_to_J      = 4.184
kcal_to_J     = cal_to_J * 1000.0

J_to_eV       = 1.0 / eV_to_J
J_to_meV      = 1.0 / meV_to_J
J_to_Ry       = 1.0 / Ry_to_J
J_to_cal      = 1.0 / cal_to_J
J_to_kcal     = 1.0 / kcal_to_J

kJmol_to_AA   = 2.809
kJmol_to_AA1  = 2.237
kJmol_to_ms   = 1.408e3
kJmol_to_K    = 120.3
kJmol_to_THz  = 2.506 
kJmol_to_rads = 1.575e13
kJmol_to_cm1  = 83.59 
kJmol_to_meV  = 10.36 

"""---
## Distance
"""

bohr_to_AA  = 5.29177210544e-1
bohr_to_m   = 5.29177210544e-11

AA_to_bohr  = 1.0 / bohr_to_AA
AA_to_m     = 1.0e-10

m_to_bohr   = 1.0 / bohr_to_m
m_to_AA     = 1.0e10

"""---
## Mass
"""
amu_to_kg   = 1.66053906660e-27
amu_to_g    = 1.66053906660e-24

kg_to_g     = 1000.0
kg_to_amu   = 1.0 / amu_to_kg

g_to_kg     = 1.0e-3
g_to_amu    = 1.0 / amu_to_g

"""---
## Pressure
"""
Pa_to_bar     = 1.0e-5
Pa_to_kbar    = 1.0e-8
Pa_to_atm     = 101325.0
Pa_to_Torr    = 760.0 / 101325.0
Pa_to_kPa     = 1.0e-3
Pa_to_mTorr   = 760000.0 / 101325.0
Pa_to_GPa     = 1.0e-9

kPa_to_bar    = 0.01
kPa_to_Pa     = 1000.0

GPa_to_bar    = 10000.0
GPa_to_kbar   = 10.0
GPa_to_Pa     = 1.0e9

bar_to_Pa     = 1.0e5
bar_to_GPa    = 1.0e-4
bar_to_atm    = 1.0 / 1.01325
bar_to_Torr   = 760.0 / 1.01325
bar_to_kbar   = 1.0e-3
bar_to_mTorr  = 760000.0 / 1.01325

kbar_to_GPa   = 0.1
kbar_to_bar   = 1000.0

atm_to_Pa     = 1 / 101325.0
atm_to_bar    = 1.01325
atm_to_Torr   = 760.0
atm_to_mTorr  = 760000.0

Torr_to_Pa    = 101325.0 / 760.0
Torr_to_bar   = 1.01325 / 760.0
Torr_to_atm   = 1.0 / 760.0
Torr_to_mTorr = 1000.0

mTorr_to_Pa   = 101325000.0 / 760.0
mTorr_to_bar  = 1013.25 / 760.0
mTorr_to_atm  = 1000.0 / 760.0
mTorr_to_Torr = 0.001

"""---
## Time
"""
H_to_s = 3600.0
s_to_H = 1.0 / H_to_s

"""---
## Wavelength
"""
AA_to_AA1   = 6.28318
AA_to_ms    = 3956
AA_to_K     = 949.3
AA_to_THz   = 19.78
AA_to_rads  = 1.243e14
AA_to_cm1   = 659.8
AA_to_meV   = 81.805
AA_to_kJmol = 7.893

"""---
## Wavevector
"""
AA1_to_AA    = 6.28318
AA1_to_ms    = 629.6
AA1_to_K     = 24.046
AA1_to_THz   = 0.5010
AA1_to_rads  = 3.148e12
AA1_to_cm1   = 16.71
AA1_to_meV   = 2.072
AA1_to_kJmol = 0.1999

"""---
## Velocity
"""
ms_to_AA    = 3956 
ms_to_AA1   = 1.589e-3
ms_to_K     = 6.066e5
ms_to_THz   = 1.265e-6
ms_to_rads  = 7.948e6
ms_to_cm1   = 4.216e-5
ms_to_meV   = 5.227e-6
ms_to_kJmol = 5.044e-7

"""---
## Temperature
"""
K_to_AA    = 30.81 
K_to_AA1   = 0.2039 
K_to_ms    = 128.4 
K_to_THz   = 0.02084 
K_to_rads  = 1.309e11
K_to_cm1   = 0.6950
K_to_meV   = 8.617e-2
K_to_kJmol = 8.314e-3

"""---
## Temperature scales
Note that to change between temperature scales,
these constants must be added instead of multiplied.
"""
C_to_K_scale = 273.15
K_to_C_scale = -C_to_K_scale

"""---
## Frequency
"""
THz_to_AA    = 4.4475
THz_to_AA1   = 1.4127 
THz_to_ms    = 889.5 
THz_to_K     = 48.0
THz_to_rads  = 6.283e12
THz_to_cm1   = 33.36 
THz_to_meV   = 4.136
THz_to_kJmol = 0.3990

"""---
## Angular frequency
"""
rads_to_AA    = 11.15e6
rads_to_AA1   = 5.64e-7
rads_to_ms    = 3.549e-4
rads_to_K     = 7.64e-12
rads_to_THz   = 0.1592e-12
rads_to_cm1   = 5.309e-12
rads_to_meV   = 6.582e-13
rads_to_kJmol = 6.351e-14

"""---
## Wavenumber
""" 
cm1_to_AA    = 25.69 
cm1_to_AA1   = 0.2446
cm1_to_ms    = 154.01
cm1_to_K     = 1.439
cm1_to_THz   = 0.02998
cm1_to_rads  = 1.884e11
cm1_to_meV   = 1.0 / meV_to_cm1
cm1_to_kJmol = 1.196e-2

