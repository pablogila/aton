"""
# Description

This module contains functions to calculate the actual `potential_values` of the system.


# Index

| | |
| --- | --- |
| `load()`        | Load a system with a custom potential from a potential file |
| `from_qe()`     | Creates a potential data file from Quantum ESPRESSO outputs |
| `interpolate()` | Interpolates the current `System.potential_values` to a new `System.gridsize` |
| `solve()`       | Solve the potential values based on the potential name |
| `zero()`        | Zero potential |
| `sine()`        | Sine potential |
| `titov2023()`   | Potential of the hidered methyl rotor, as in titov2023. |

---
"""


from .system import System
from . import constants
import numpy as np
import os
from copy import deepcopy
from scipy.interpolate import CubicSpline
import aton.st.alias as alias
import aton.st.file as file
import aton.interface.qe as qe
import aton.phys as phys
from aton._version import __version__


def load(
        filepath:str='potential.dat',
        system:System=None,
        angle_unit:str='deg',
        energy_unit:str='meV',
        ) -> System:
    """Read a potential rotational energy dataset.

    The file in `filepath` should contain two columns with angle and potential energy values.
    Degrees and meV are assumed as default units unless stated in `angle_unit` and `energy_unit`.
    Units will be converted automatically to radians and meV.
    """
    file_path = file.get(filepath)
    system = System() if system is None else system
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
    if energy_unit.lower() in alias.units['eV']:
        potentials = np.array(potentials) * phys.eV_to_meV
    elif energy_unit.lower() in alias.units['meV']:
        potentials = np.array(potentials)
    elif energy_unit.lower() in alias.units['Ry']:
        potentials = np.array(potentials) * phys.Ry_to_meV
    else:
        raise ValueError(f"Energy unit '{energy_unit}' not recognized.")
    # Set the system
    system.grid = np.array(positions)
    system.gridsize = len(positions)
    system.potential_values = np.array(potentials)
    # System comment as the parent folder name
    system.comment = os.path.basename(os.path.dirname(file_path))
    return system


def from_qe(
        folder=None,
        output:str='potential.dat',
        include:list=['.out'],
        ignore:list=['slurm-'],
        energy_unit:str='meV',
        ) -> None:
    """Creates a potential data file from Quantum ESPRESSO outputs.

    The angle in degrees is extracted from the output filenames,
    which must follow `whatever_ANGLE.out`.

    Outputs from SCF calculations must be located in the provided `folder` (CWD if None).
    Files can be filtered by those containing the specified `filters`,
    excluding those containing any string from the `ignore` list. 
    The `output` name is `potential.dat` by default.

    Energy values are saved to meV by dafault, unless specified in `energy_unit`.
    """
    folder = file.get_dir(folder)
    # Check if a previous potential.dat file exists, and ask to overwrite it
    previous_potential_file = file.get(output, return_anyway=True)
    if previous_potential_file:
        print(f"WARNING: Previous '{output}' file will be overwritten, proceed anyway?")
        answer = input("(y/n): ")
        if not answer.lower() in alias.boolean[True]:
            print("Aborted.")
            return None
    # Get the files to read
    files = file.get_list(folder=folder, include=include, ignore=ignore, abspath=True)
    folder_name = os.path.basename(folder)
    # Set header
    potential_data = f'# Potential from calculation {folder_name}\n'
    potential_data += f'# Imported with ATON {__version__}\n'
    potential_data += '# https://pablogila.github.io/ATON\n'
    potential_data += '#\n'
    if energy_unit.lower() in alias.units['eV']:
        potential_data += '# Angle/deg    Potential/eV\n'
    elif energy_unit.lower() in alias.units['meV']:
        potential_data += '# Angle/deg    Potential/meV\n'
    elif energy_unit.lower() in alias.units['Ry']:
        potential_data += '# Angle/deg    Potential/Ry\n'
    else:
        potential_data += '# Angle/deg    Potential/meV\n'
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
        if energy_unit.lower() in alias.units['eV']:
            energy = content['Energy'] * phys.Ry_to_eV
        elif energy_unit.lower() in alias.units['meV']:
            energy = content['Energy'] * phys.Ry_to_meV
        elif energy_unit.lower() in alias.units['Ry']:
            energy = content['Energy']
        else:
            print(f"WARNING: Energy unit '{energy_unit}' not recognized, using meV instead.")
            energy = content['Energy'] * phys.Ry_to_meV
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


def interpolate(system:System) -> System:
    """Interpolates the current `System.potential_values`
    to a new grid of size `System.gridsize`.
    """
    print(f"Interpolating potential to a grid of size {system.gridsize}...")
    V = system.potential_values
    grid = system.grid
    gridsize = system.gridsize
    new_grid = np.linspace(0, 2*np.pi, gridsize)
    cubic_spline = CubicSpline(grid, V)
    new_V = cubic_spline(new_grid)
    system.grid = new_grid
    system.potential_values = new_V
    return system


# Redirect to the desired potential energy function
def solve(system:System):
    """Solves `System.potential_values`
    according to the `System.potential_name`,
    returning the new `potential_values`.
    Avaliable potential names are `zero`, `sine` and `titov2023`.

    If `System.potential_name` is not present or not recognised,
    the current `System.potential_values` are used.

    If a bigger `System.gridsize` is provided,
    the potential is also interpolated to the new gridsize.

    This function provides basic solving of the potential energy function.
    To interpolate to a new grid and correct the potential offset after solving,
    check `aton.qrotor.solve.potential()`.
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


def zero(system:System):
    """Zero potential."""
    x = system.grid
    return 0 * x


def sine(system:System):
    """Sine potential.

    $C_0 + C_1 sin(3x + C_2)$  
    If no `System.potential_constants` are provided, defaults to $sin(3x)$  
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


def titov2023(system:System):
    """Potential energy function of the hindered methyl rotor, from
    [K. Titov et al., Phys. Rev. Mater. 7, 073402 (2023)](https://link.aps.org/doi/10.1103/PhysRevMaterials.7.073402).  

    $C_0 + C_1 sin(3x) + C_2 cos(3x) + C_3 sin(6x) + C_4 cos(6x)$  
    Default constants are `aton.qrotor.constants.constants_titov2023`[0].  
    """
    x = system.grid
    C = system.potential_constants
    if C is None:
        C = constants.constants_titov2023[0]
    return C[0] + C[1] * np.sin(3*x) + C[2] * np.cos(3*x) + C[3] * np.sin(6*x) + C[4] * np.cos(6*x)

