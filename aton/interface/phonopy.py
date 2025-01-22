"""
# Description

Functions to work with [Phonopy](https://phonopy.github.io/phonopy/) calculations,
along with [Quantum ESPRESSO](https://www.quantum-espresso.org/).  


# Index

| | |
| --- | --- |
| `make_supercells()` | Build supercell SCF inputs for phonon calculations |


# Examples

To create the supercells and run the phonon calculations
from a folder with `relax.in` and `relax.out` files,
using a `template.slurm` file,
```python
from aton import interface
interface.phonopy.make_supercells()
interface.slurm.sbatch('supercell-', 'scf.slurm')
```

---
"""


import os
import re
from aton._version import __version__
import aton.st.file as file
import aton.st.call as call
import aton.txt.find as find
import aton.txt.edit as edit # text
import aton.txt.extract as extract
import aton.interface.qe as qe
import aton.interface.slurm as slurm


def make_supercells(
        dimension:str='2 2 2',
        relax_in:str='relax.in',
        relax_out:str='relax.out',
        folder:str=None,
        slurm_template:str=None,
    ) -> None:
    """
    Creates the supercell inputs of a given `dimension` ('2 2 2' by default),
    from the `relax_in` and `relax_out` files in the `folder`
    ('relax.in', 'relax.out' and CWD by default, respectively),
    needed for the Phonopy calculations with Quantum ESPRESSO.

    If `slurm_template` is present,
    it checks it with `aton.interface.slurm.check_template()`.
    """
    print(f'\nWelcome to thotpy.phonopy {__version__}\n'
          'Creating all supercell inputs with Phonopy for Quantum ESPRESSO...\n')
    qe.scf_from_relax(folder, relax_in, relax_out)
    _supercells_from_scf(dimension, folder)
    _copy_scf_header_to_supercells(folder)
    print('\n------------------------------------------------------\n'
          'PLEASE CHECH BELOW THE CONTENT OF THE supercell-001.in\n'
          '------------------------------------------------------\n')
    call.bash('head -n 100 supercell-001.in')
    print('\n------------------------------------------------------\n'
          'PLEASE CHECH THE CONTENT OF THE supercell-001.in\n'
          'The first 100 lines of the input were printed above!\n'
          '------------------------------------------------------\n\n'
          'If it seems correct, run the calculations with thotpy.phonopy.sbatch()\n')
    if slurm_template:
        slurm.check_template(slurm_template, folder)
    return None


def _supercells_from_scf(
        dimension:str='2 2 2',
        folder:str=None,
        scf:str='scf.in'
    ) -> None:
    """
    Creates supercells of a given `dimension` (`2 2 2` by default) inside a `folder`,
    from a Quantum ESPRESSO `scf` input (`scf.in` by default).
    """
    print(f'\naton.interface.phonopy {__version__}\n')
    folder = call.here(folder)
    scf_in = file.get(folder, scf, True)
    if scf_in is None:
        raise ValueError('No SCF input found in path!')
    call.bash(f'phonopy --qe -d --dim="{dimension}" -c {scf_in}')
    return None


def _copy_scf_header_to_supercells(
        folder:str=None,
        scf:str='scf.in',
    ) -> None:
    """Paste the header from the `scf` file in `folder` to the supercells created by Phonopy."""
    print(f'\naton.interface.phonopy {__version__}\n'
          f'Adding headers to Phonopy supercells for Quantum ESPRESSO...\n')
    folder = call.here(folder)
    # Check if the header file, the scf.in, exists
    scf_file = file.get(folder, scf, True)
    if scf_file is None:
        raise ValueError('No header file found in path!')
    # Check if the supercells exist
    supercells = file.get_list(folder, include='supercell-')
    if supercells is None:
        raise ValueError('No supercells found in path!')
    # Check if the supercells contains '&CONTROL' and abort if so
    supercell_sample = supercells[0]
    is_control = find.lines(supercell_sample, r'(&CONTROL|&control)', 1, 0, False, True)
    if is_control:
        raise ValueError('Supercells already contain &CONTROL! Did you do this already?')
    # Check if the keyword is in the scf file
    is_header = find.lines(scf_file, r'ATOMIC_SPECIES', 1, 0, False, False)
    if not is_header:
        raise ValueError('No ATOMIC_SPECIES found in header!')
    # Copy the scf to a temp file
    temp_scf = '_scf_temp.in'
    file.copy(scf_file, temp_scf)
    # Remove the top content from the temp file
    edit.delete_under(temp_scf, 'K_POINTS', -1, 2, False)
    # Find the new number of atoms and replace the line
    updated_values = find.lines(supercell_sample, 'ibrav', 1)  # !    ibrav = 0, nat = 384, ntyp = 5
    if not updated_values:
        print("!!! Okay listen, this is weird. This code should never be running, "
              "but for some reson we couldn't find the updated values in the supercells. "
              "Please, introduce the NEW NUMBER OF ATOMS in the supercells manually (int):")
        nat = int(input('nat = '))
    else:
        nat = extract.number(updated_values[0], 'nat')
    qe.set_value(temp_scf, 'nat', nat)
    # Remove the lattice parameters, since Phonopy already indicates units
    qe.set_value(temp_scf, 'celldm(1)', '')
    qe.set_value(temp_scf, 'A', '')
    qe.set_value(temp_scf, 'B', '')
    qe.set_value(temp_scf, 'C', '')
    qe.set_value(temp_scf, 'cosAB', '')
    qe.set_value(temp_scf, 'cosAC', '')
    qe.set_value(temp_scf, 'cosBC', '')
    # Add the header to the supercells
    with open(temp_scf, 'r') as f:
        header = f.read()
    for supercell in supercells:
        edit.insert_at(supercell, header, 0)
    # Remove the temp file
    os.remove('_scf_temp.in')
    print('Done!')
    return None

