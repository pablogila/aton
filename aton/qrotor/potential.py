"""
# Description

This module contains functions to calculate the actual `potential_values` of the system.


# Index

| | |
| --- | --- |
| `load()`        | Load a system with a custom potential from a potential file |
| `from_qe()`     | Creates a potential data file from Quantum ESPRESSO outputs |
| `interpolate()` | Interpolates the current `QSys.potential_values` to a new `QSys.gridsize` |
| `solve()`       | Solve the potential values based on the potential name |
| `zero()`        | Zero potential |
| `sine()`        | Sine potential |
| `titov2023()`   | Potential of the hidered methyl rotor, as in titov2023. |

---
"""


from .classes import *
from . import constants
import numpy as np
import os
from copy import deepcopy
from scipy.interpolate import CubicSpline
import aton.st.alias as alias
import aton.st.file as file
import aton.interface.qe as qe
import aton.phys as phys


def load(
        filepath:str='potential.dat',
        system:QSys=None,
        angle_unit:str='deg',
        energy_unit:str='eV',
        ) -> QSys:
    """Read a potential rotational energy dataset.

    The file in `filepath` should contain two columns with angle and potential energy values.
    Degrees and eV are assumed as default units unless stated in `angle_unit` and `energy_unit`.
    Units will be converted automatically to radians and eV.
    """
    file_path = file.get(filepath)
    system = QSys() if system is None else system
    with open(file_path, 'r') as f:
        lines = f.readlines()
    positions = []
    potentials = []
    for line in lines:
        if line.startswith('#'):
            continue
        position, potential = line.split()
        positions.append(float(position.strip()))
        potentials.append(float(potential.strip()))
    # Save angles to numpy arrays
    if angle_unit.lower() in alias.units['deg']:
        positions = np.radians(positions)
    elif angle_unit.lower() in alias.units['rad']:
        positions = np.array(positions)
    else:
        raise ValueError(f"Angle unit '{angle_unit}' not recognized.")
    # Save energies to numpy arrays
    if energy_unit.lower() in alias.units['meV']:
        potentials = np.array(potentials) * 1000
    elif energy_unit.lower() in alias.units['eV']:
        potentials = np.array(potentials)
    elif energy_unit.lower() in alias.units['Ry']:
        potentials = np.array(potentials) * phys.Ry_to_eV
    else:
        raise ValueError(f"Energy unit '{energy_unit}' not recognized.")
    # Set the system
    system.grid = np.array(positions)
    system.gridsize = len(positions)
    system.potential_values = np.array(potentials)
    return system


def from_qe(
        folder=None,
        output:str='potential.dat',
        include:list=['.out'],
        ignore:list=['slurm-'],
        ) -> None:
    """Creates a potential data file from Quantum ESPRESSO outputs.

    The angle in degrees is extracted from the output filenames,
    which must follow `whatever_ANGLE.out`.

    Outputs from SCF calculations must be located in the provided `folder` (CWD if None).
    Files can be filtered by those containing the specified `filters`,
    excluding those containing any string from the `ignore` list. 
    The `output` name is `potential.dat` by default.
    """
    folder = file.get_dir(folder)
    files = file.get_list(folder=folder, include=include, ignore=ignore, abspath=True)
    potential_data = '# Angle/deg    Potential/eV\n'
    potential_data_list = []
    print('Extracting the potential as a function of the angle...')
    print('----------------------------------')
    counter_success = 0
    counter_errors = 0
    for filepath in files:
        filename = os.path.basename(filepath)
        filepath = file.get(filepath=filepath, include='.out', return_anyway=True)
        if not filepath:  # Not an output file, skip it
            continue
        content = qe.read_out(filepath)
        if not content['Success']:  # Ignore unsuccessful calculations
            print(f'x   {filename}')
            counter_errors += 1
            continue
        energy = content['Energy'] * phys.Ry_to_eV
        splits = filename.split('_')
        angle = splits[-1].replace('.out', '')
        angle = float(angle)
        potential_data_list.append((angle, energy))
        print(f'OK  {filename}')
        counter_success += 1
    # Sort by angle
    potential_data_list_sorted = sorted(potential_data_list, key=lambda x: x[0])
    # Append the sorted values as a string
    for angle, energy in potential_data_list_sorted:
        potential_data += f'{angle}    {energy}\n'
    with open(output, 'w') as f:
        f.write(potential_data)
    print('----------------------------------')
    print(f'Succesful calculations (OK): {counter_success}')
    print(f'Faulty calculations     (x): {counter_errors}')
    print('----------------------------------')
    print(f'Saved angles and potential values at {output}')
    return None


def interpolate(system:QSys) -> QSys:
    """Interpolates the current `aton.qrotor.classes.QSys.potential_values` to a new grid of size `aton.qrotor.classes.QSys.gridsize`."""
    V = system.potential_values
    grid = system.grid
    gridsize = system.gridsize
    new_grid = np.linspace(0, 2*np.pi, gridsize)
    cubic_spline = CubicSpline(grid, V)
    new_V = cubic_spline(new_grid)
    system.grid = new_grid
    system.potential_values = new_V
    print(f"Interpolated potential to a grid of size {gridsize}")
    return system


# Redirect to the desired potential energy function
def solve(system:QSys):
    """Solves `aton.qrotor.classes.QSys.potential_values`,
    according to the `aton.qrotor.classes.QSys.potential_name`.
    Returns the new `potential_values`.

    If `QSys.potential_name` is not present or not recognised,
    the current `QSys.potential_values` are used.

    If a bigger `QSys.gridsize` is provided,
    the potential is also interpolated to the new gridsize.
    """
    data = deepcopy(system)
    # Is there a potential_name?
    if not data.potential_name:
        if not any(data.potential_values):
            raise ValueError(f'No potential_name and no potential_values found in the system!')
    elif data.potential_name.lower() == 'titov2023':
        data.potential_values = titov2023(data)
    elif data.potential_name.lower() == 'zero':
        data.potential_values = zero(data)
    elif data.potential_name.lower() == 'sine':
        data.potential_values = sine(data)
    # At least there should be potential_values
    elif not any(data.potential_values):
        raise ValueError("Unrecognised potential_name '{data.potential_name}' and no potential_values found")
    return data.potential_values


def zero(system:QSys):
    """Zero potential."""
    x = system.grid
    return 0 * x


def sine(system:QSys):
    """Sine potential.

    If potential_constants are provided, returns:
    $C_0 + C_1 sin(3x + C_2)$.
    """
    x = system.grid
    C = system.potential_constants
    C0 = 0
    C1 = 1
    C2 = 0
    if C:
        if len(C) > 0:
            C0 = C[0]
        if len(C) > 1:
            C1 = C[1]
        if len(C) > 2:
            C2 = C[2]
    return C0 + C1 * np.sin(3*x + C2)


def titov2023(system:QSys):
    """Potential energy function of the hindered methyl rotor, from titov2023."""
    x = system.grid
    C = system.potential_constants
    if C is None:
        C = constants.constants_titov2023[0]
    return C[0] + C[1] * np.sin(3*x) + C[2] * np.cos(3*x) + C[3] * np.sin(6*x) + C[4] * np.cos(6*x)

