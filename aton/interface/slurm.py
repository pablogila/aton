"""
# Description

Functions to handle SLURM calls, to run calculations in clusters.  


# Index

| | |
| --- | --- |
| `sbatch()`         | Sbatch'es calculations |
| `check_template()` | Checks that the slurm template is OK, and provides an example if not |

---
"""


import os
import aton.st.call as call
import aton.st.file as file
import aton.text.find as find
import aton.text.edit as edit
from aton._version import __version__


def sbatch(
        prefix:str,
        template:str='template.slurm',
        in_ext:str='.in',
        out_ext:str='.out',
        folder=None,
        testing:bool=False,
    ) -> None:
    """Launch all your calculations to a cluster using the SLURM manager.

    Calculation names should follow `prefix_ID.ext`,
    with `prefix` as the common name across calculations,
    followed by the calculation ID, used as JOB_NAME.
    The extensions from `in_ext` and `out_ext` ('.in' and '.out' by default)
    will be used for the INPUT_FILE and OUTPUT_FILE of the slurm template.

    The slurm template, `template.slurm` by default,
    must contain the keywords JOB_ID, INPUT_FILE and OUTPUT_FILE:
    ```
    #SBATCH --job-name=JOB_NAME
    mpirun pw.x -inp INPUT_FILE > OUTPUT_FILE
    ```

    Runs from the specified `folder`, current working directory if empty.

    If `testing = True` it skips the final sbatching,
    just printing the commands on the screen.
    """
    print(f'\naton.interface.slurm {__version__}\n'
          'Sbatching all calculations...\n')
    key_input = 'INPUT_FILE'
    key_output = 'OUTPUT_FILE'
    key_jobname = 'JOB_NAME'
    slurm_folder = 'slurms'
    folder = call.here(folder)
    # Get input files and abort if not found
    inputs_raw = file.get_list(folder=folder, filters=prefix, abspath=False)
    inputs = []
    for filename in inputs_raw:
        if filename.endswith(in_ext):
            inputs.append(filename)
    if len(inputs) == 0:
        raise FileNotFoundError(f"Input files were not found! Expected {prefix}-ID.{in_ext} (ID separator can be '_', '-' or '.')")
    call.bash(f"mkdir {slurm_folder}", folder, True, True)
    # Get the template
    slurm_file = check_template(template, folder)
    if not slurm_file:
        print(f'Aborting... Please correct {template}\n')
        return None
    for filename in inputs:
        # Get the file ID
        basename: str = os.path.basename(filename)
        basename_out: str = basename.replace(in_ext, out_ext)
        calc_id = basename.replace(prefix, '')
        calc_id = calc_id.replace(in_ext, '')
        calc_id = calc_id.replace('_', '')
        calc_id = calc_id.replace('-', '')
        calc_id = calc_id.replace('.', '')
        # Create slurm file for this supercell
        slurm_id = prefix + calc_id + '.slurm'
        # fixing dictionary with the words to replace in the template
        fixing_dict = {
            key_jobname: calc_id,
            key_input: basename,
            key_output: basename_out
        }
        edit.from_template(slurm_file, slurm_id, fixing_dict)
        if testing:
            call.bash(f"echo {slurm_id}", folder)
        else:
            call.bash(f"sbatch {slurm_id}", folder, True, False)
        call.bash(f"mv {slurm_id} {slurm_folder}", folder, False, True)  # Do not raise error if we can't move the file
    print(f'\nDone! Temporary slurm files were moved to /{slurm_folder}/\n')


def check_template(
        template:str='template.slurm',
        folder=None,
    ) -> str:
    """Check the slurm `template` inside `folder`.

    The current working directory is used if `folder` is not provided.
    If the file does not exist or is invalid, creates a `template_EXAMPLE.slurm` file for reference.
    """
    folder = call.here(folder)
    slurm_example = 'template_EXAMPLE.slurm'
    new_slurm_file = os.path.join(folder, slurm_example)
    # Default slurm template
    content =f'''# Automatic slurm template created with aton.interface.slurm {__version__}\n# https://github.com/pablogila/ATON
#!/bin/bash
#SBATCH --partition=general
#SBATCH --qos=regular
#SBATCH --job-name=JOB_NAME
#SBATCH --ntasks=32
#SBATCH --time=1-00:00:00
#SBATCH --mem=128G
# #SBATCH --mail-user=YOUR@EMAIL
# #SBATCH --mail-type=END

module purge
module load QuantumESPRESSO/7.3-foss-2023a

mpirun pw.x -inp INPUT_FILE > OUTPUT_FILE
'''
    # If the slurm template does not exist, create one
    slurm_file = file.get(folder, template, True)
    if not slurm_file:
        with open(new_slurm_file, 'w') as f:
            f.write(content)
        print(f'!!! WARNING:  Slurm template missing, so an example was generated automatically:\n'
              f'{slurm_example}\n'
              f'PLEASE CHECK it, UPDATE it and RENAME it to {template}\n'
              'before running aton.interface.phonopy.sbatch()\n')
        return None
    # Check that the slurm file contains the INPUT_FILE, OUTPUT_FILE and JOB_NAME keywords
    key_input = find.lines(slurm_file, 'INPUT_FILE')
    key_output = find.lines(slurm_file, 'OUTPUT_FILE')
    key_jobname = find.lines(slurm_file, 'JOB_NAME')
    missing = []
    if not key_input:
        missing.append('INPUT_FILE')
    if not key_output:
        missing.append('OUTPUT_FILE')
    if not key_jobname:
        missing.append('JOB_NAME')
    if len(missing) > 0:
        with open(new_slurm_file, 'w') as f:
            f.write(content)
        print('!!! WARNING:  Some keywords were missing from your slurm template,\n'
              f'PLEASE CHECK the example at {slurm_example}\n'
              'before running aton.interface.slurm.sbatch()\n'
              f'The following keywords were missing from your {template}:')
        for key in missing:
            print(key)
        print('')
        return None
    return slurm_file  # Ready to use!

