"""
# Description

Functions to handle Slurm calls, to run calculations in clusters.  


# Index

| | |
| --- | --- |
| `sbatch()`         | Sbatch all calculations |
| `squeue()`         | Get a Pandas DataFrame with info about the submitted calculations |
| `scancel()`        | Scancel all calculations, or applying some filters |
| `scancel_here()`   | Scancel all calculations running from a specific folder |
| `check_template()` | Checks that the slurm template is OK, and provides an example if not |

---
"""


import os
import pandas as pd
import aton.st.call as call
import aton.st.file as file
import aton.txt.find as find
import aton.txt.edit as edit
from aton._version import __version__


def sbatch(
        prefix:str='',
        template:str='template.slurm',
        in_ext:str='.in',
        out_ext:str='.out',
        folder=None,
        files:list=[],
        testing:bool=False,
    ) -> None:
    """Sbatch all the calculations at once.

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

    If more control is required, a custom list of `files` can be specified for sbatching.

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
    if not files:
        inputs_raw = file.get_list(folder=folder, include=prefix, abspath=False)
    else:
        inputs_raw = files
    inputs = []
    for filename in inputs_raw:
        if filename.endswith(in_ext):
            inputs.append(filename)
    if len(inputs) == 0:
        raise FileNotFoundError(f"Input files were not found! Expected {prefix}ID.{in_ext}")
    # Make the folder for the sbatch'ed slurm files
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
    print(f'\nDone! Temporary slurm files were moved to ./{slurm_folder}/\n')


def squeue(user) -> pd.DataFrame:
    result = call.bash(command=f'squeue -u {user}', verbose=False)
    data = result.stdout
    lines = data.strip().split('\n')
    data_rows = [line.split() for line in lines[1:]]
    df = pd.DataFrame(data_rows, columns=lines[0].split())
    return df


def scancel(
        user:str,
        status:str='',
        text:str='',
        testing:bool=False,
        key_jobid:str='JOBID',
        key_name:str='NAME',
        key_status:str='ST',
        ) -> None:
    """Cancel all `user` jobs.
    
    If a particular `status` string is provided,
    only the calculations with said status will be cancelled.

    If a particular `text` string is provided,
    only the calculations containing said text in the name will be deleted.

    If `testing = True`, it shows the calculations that would be deleted.

    if the slurm squeue titles are different in your cluster,
    you can specify them with `key_jobid`, `key_status` and `key_name`.
    """
    df = squeue(user)
    if testing:
        print('aton.interface.slurm.scancel(testing=True):')
        print(f'The following calculations would be deleted for the user {user}')
        print(f'{key_jobid}   {key_status}   {key_name}')
    jobid_list = df[key_jobid].tolist()
    name_list = df[key_name].tolist()
    status_list = df[key_status].tolist()
    for i, jobid in enumerate(jobid_list):
        name = name_list[i]
        st = status_list[i]
        # Should we delete this process?
        bool_1: bool = status == '' and text == ''
        bool_2: bool = status == st and text == ''
        bool_3: bool = status == '' and text in name
        bool_4: bool = status == st and text in name
        will_delete: bool = bool_1 or bool_2 or bool_3 or bool_4
        if will_delete:
            if testing:
                print(f'{jobid}   {st}   {name}')
            else:
                call.bash(f'scancel {jobid}')


def scancel_here(jobs=None, folder=None, prefix:str='slurm-', sufix:str='.out') -> None:
    """Cancel all running `jobs` in a given `folder`.

    If no job is provided, all jobs detected in the current folder will be cancelled.
    The jobs will be detected from the `<prefix>JOBID<sufix>` files, `slurm-JOBID.out` by default.
    """
    if jobs == None:  # Get the list of jobs
        filenames = file.get_list(folder=folder, include=prefix, abspath=False)
        if not filenames:
            raise FileNotFoundError(f'To scancel all calculations, {prefix}JOBID{sufix} files are needed!\nConfigure the folder, as well as the prefix and sufix if necessary.')
        jobs = []
        for filename in filenames:
            filename = filename.replace(prefix, '')
            filename = filename.replace(sufix, '')
            jobs.append(filename)
    if isinstance(jobs, str):
        jobs = [jobs]
    if not isinstance(jobs, list):
        raise ValueError(f'Input jobs must be a string or a list of strings! Yours was: {type(jobs)}')
    for job in jobs:
        call.bash(f'scancel {job}', folder)
    return None


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

