"""
# Description

Functions to work with [Phonopy](https://phonopy.github.io/phonopy/) calculations,
along with [Quantum ESPRESSO](https://www.quantum-espresso.org/).  


# Index

| | |
| --- | --- |
| `make_supercells()` | Build supercell SCF inputs for phonon calculations |


# Examples

To create the 2x2x2 supercells and run the phonon calculations
from a folder with `relax.in` and `relax.out` files,
using a `template.slurm` file,
```python
from aton import api
api.phonopy.make_supercells()
api.slurm.sbatch('supercell-', 'template.slurm')
```

---
"""


import os
from aton._version import __version__
import aton.file as file
import aton.call as call
import aton.txt.find as find
import aton.txt.edit as edit # text
import aton.txt.extract as extract
import aton.api.qe as qe
import aton.api.slurm as slurm


def make_supercells(
        dimension:str='2 2 2',
        relax_in:str='relax.in',
        relax_out:str='relax.out',
        folder:str=None,
        slurm_template:str='template.slurm',
    ) -> None:
    """
    Creates the supercell inputs of a given `dimension` ('2 2 2' by default),
    from the `relax_in` and `relax_out` files in the `folder`
    ('relax.in', 'relax.out' and CWD by default, respectively),
    needed for the Phonopy calculations with Quantum ESPRESSO.

    By default, at the end of the execution it will check
    that an `slurm_template` ('template.slurm') is present and valid;
    this is, containing the keywords `JOBNAME`, `INPUT` and `OUTPUT`.
    If not, an example with instructions will be provided.
    This check can be skipped with `slurm_template=''`.
    The template will allow to easily run the Phonopy calculations with the one-line command
    `aton.api.slurm.sbatch('supercell-', 'template.slurm')`
    """
    print(f'\nWelcome to aton.api.phonopy {__version__}\n'
          'Creating all supercell inputs with Phonopy for Quantum ESPRESSO...\n')
    qe.scf_from_relax(folder, relax_in, relax_out)
    _supercells_from_scf(dimension, folder)
    _copy_scf_header_to_supercells(folder)
    print('\n------------------------------------------------------\n'
          'PLEASE CHECH BELOW THE CONTENT OF supercell-001.in\n'
          '------------------------------------------------------\n')
    call.bash('head -n 100 supercell-001.in')
    print('\n------------------------------------------------------\n'
          'PLEASE CHECH THE CONTENT OF supercell-001.in\n'
          'The first 100 lines of the input were printed above!\n'
          '------------------------------------------------------\n\n'
          'If it seems correct, run the calculations with:\n'
          f"aton.api.slurm.sbatch('supercell-', '{slurm_template}')\n")
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
    print(f'\naton.api.phonopy {__version__}\n')
    folder = call.here(folder)
    scf_in = file.get(folder, scf, True)
    if scf_in is None:
        raise FileNotFoundError('No SCF input found in path!')
    call.bash(f'phonopy --qe -d --dim="{dimension}" -c {scf_in}')
    return None


def _copy_scf_header_to_supercells(
        folder:str=None,
        scf:str='scf.in',
    ) -> None:
    """Paste the header from the `scf` file in `folder` to the supercells created by Phonopy."""
    print(f'\naton.api.phonopy {__version__}\n'
          f'Adding headers to Phonopy supercells for Quantum ESPRESSO...\n')
    folder = call.here(folder)
    # Check if the header file, the scf.in, exists
    scf_file = file.get(folder, scf, True)
    if scf_file is None:
        raise FileNotFoundError('No header file found in path!')
    # Check if the supercells exist
    supercells = file.get_list(folder, include='supercell-')
    if supercells is None:
        raise FileNotFoundError('No supercells found in path!')
    # Check if the supercells contains '&CONTROL' and abort if so
    supercell_sample = supercells[0]
    is_control = find.lines(supercell_sample, r'(&CONTROL|&control)', 1, 0, False, True)
    if is_control:
        raise RuntimeError('Supercells already contain &CONTROL! Did you do this already?')
    # Check if the keyword is in the scf file
    is_header = find.lines(scf_file, r'ATOMIC_SPECIES', 1, 0, False, False)
    if not is_header:
        raise RuntimeError('No ATOMIC_SPECIES found in header!')
    # Copy the scf to a temp file
    temp_scf = '_scf_temp.in'
    file.copy(scf_file, temp_scf)
    # Remove the top content from the temp file
    edit.delete_under(temp_scf, 'K_POINTS', -1, 2, False)
    # Find the new number of atoms and replace the line
    updated_values = find.lines(supercell_sample, 'ibrav', 1)  # !    ibrav = 0, nat = 384, ntyp = 5
    if not updated_values:
        print("!!! Okay listen, this is weird. This line of code should never be running, "
              "but for some reson I couldn't find the updated values in the supercells. "
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

