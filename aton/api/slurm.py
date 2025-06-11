"""
# Description

Functions to handle Slurm calls, to run calculations in clusters.  


# Index

| | |
| --- | --- |
| `sbatch()`           | Sbatch all calculations |
| `squeue()`           | Get a Pandas DataFrame with info about the submitted calculations |
| `scancel()`          | Scancel all calculations, or applying some filters |
| `scancel_errors()`   | Scancel calculations with specific errors |
| `scancel_here()`     | Scancel all calculations running from a specific folder |
| `get_running_here()` | Get a list with all jobs running in a given folder |
| `check_template()`   | Checks that the slurm template is OK, and provides an example if not |

---
"""


import os
import pandas as pd
import aton.call as call
import aton.file as file
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
    will be used for the INPUT and OUTPUT filenames of the slurm template.

    The slurm template, `template.slurm` by default,
    must contain the keywords `JOBNAME`, `INPUT` and `OUTPUT`:
    ```
    #SBATCH --job-name=JOBNAME
    srun --cpu_bind=cores pw.x -inp INPUT > OUTPUT
    ```

    Runs from the specified `folder`, current working directory if empty.

    If more control is required, a custom list of `files` can be specified for sbatching.

    If `testing = True` it skips the final sbatching,
    just printing the commands on the screen.
    """
    print('Sbatching all calculations...\n')
    key_input = 'INPUT'
    key_output = 'OUTPUT'
    key_jobname = 'JOBNAME'
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
    print(f'Done! Temporary slurm files were moved to ./{slurm_folder}/\n')


def squeue(user) -> pd.DataFrame:
    """Returns a Pandas DataFrame with the jobs from a specific `user`"""
    result = call.bash(command=f'squeue -u {user}', verbose=False)
    data = result.stdout
    lines = data.strip().split('\n')
    data_rows = [line.split() for line in lines[1:]]
    df = pd.DataFrame(data_rows, columns=lines[0].split())
    return df


def scancel(
        user:str,
        text:str='',
        status:str='',
        jobs:list=[],
        key_jobid:str='JOBID',
        key_name:str='NAME',
        key_status:str='ST',
        testing:bool=False,
        ) -> None:
    """Cancel all `user` jobs.

    If a particular `text` string is provided,
    only the calculations containing said string in the name will be deleted.

    If a particular `status` string is provided,
    only the calculations with said status will be cancelled.

    If a list of `jobs` is provided, those JOBIDs will be cancelled.

    These filters can all be combined to provide strict control.

    If `testing = True`, it shows the calculations that would be deleted.

    if the slurm squeue titles are different in your cluster,
    you can specify them with `key_jobid`, `key_status` and `key_name`.
    """
    df = squeue(user)
    if testing:
        print('aton.api.slurm.scancel(testing=True):')
        print(f'The following calculations would be killed for the user {user}')
        print(f'{key_jobid}   {key_status}   {key_name}')
    jobid_list = df[key_jobid].tolist()
    name_list = df[key_name].tolist()
    status_list = df[key_status].tolist()
    for i, jobid in enumerate(jobid_list):
        name = name_list[i]
        st = status_list[i]
        job = jobid_list[i]
        # Should we delete this process?
        bool_1: bool = status == '' and text == ''
        bool_2: bool = status == st and text == ''
        bool_3: bool = status == '' and text in name
        bool_4: bool = status == st and text in name
        will_delete: bool = bool_1 or bool_2 or bool_3 or bool_4
        if jobs:
            jobs = [str(i).strip() for i in jobs]
            will_delete = will_delete and job in jobs
        if will_delete:
            if testing:
                print(f'{jobid}   {st}   {name}')
            else:
                call.bash(f'scancel {jobid}')


def scancel_errors(
        user:str='',
        errors=['oom_killed', 'OOM Killed', 'Out Of Memory'],
        folder=None,
        prefix:str='slurm-',
        sufix:str='.out',
        key_jobid:str='JOBID',
        testing=False,
        ) -> None:
    """Cancel all running jobs with any matching `errors` in a given `folder`.

    By default it matches Out Of Memory errors (OOM).
    The jobs will be detected from the `<prefix>JOBID<sufix>` files, `slurm-JOBID.out` by default.

    If an `user` name is provided, it additionally checks if the jobs are actually scheduled
    to avoid reporting or killing jobs that have already finished.
    If the slurm squeue 'JOBID' title is different in your cluster,
    change it with `key_jobid`.

    If `testing=True`, it will only print the jobs that would be cancelled.
    """
    filenames = get_running_here(user=user, folder=folder, prefix=prefix, sufix=sufix, key_jobid=key_jobid, get_files=True)
    filenames_to_cancel = []
    jobs_to_cancel = []
    # Ensure errors is a list
    if not isinstance(errors, list):
        errors = [str(errors)]
    # Find errors in the slurm files
    for f in filenames:
        matches = []
        for e in errors:
            m = find.lines(filepath=f, key=e)
            matches.extend(m)
        if matches:
            filenames_to_cancel.append(f)
    # Convert filenames to JOBIDs
    for f in filenames_to_cancel:
        f = f.replace(prefix, '')
        f = f.replace(sufix, '')
        jobs_to_cancel.append(f)
    # Report or scancel
    if testing:
        print('The following jobs would be cancelled:')
        for job in jobs_to_cancel:
            print(f'{job}')
        return None
    for job in jobs_to_cancel:
        call.bash(f'scancel {job}', folder)
    return None


def scancel_here(
        user:str='',
        folder=None,
        prefix:str='slurm-',
        sufix:str='.out',
        key_jobid:str='JOBID',
        testing:bool=False,
        ) -> None:
    """Cancel all running jobs in a given `folder`.

    The jobs will be detected from the `<prefix>JOBID<sufix>` files, `slurm-JOBID.out` by default.

    If an `user` name is provided, it additionally checks if the jobs are actually scheduled
    to avoid reporting or killing jobs that have already finished.
    If the slurm squeue 'JOBID' title is different in your cluster,
    change it with `key_jobid`.

    If `testing=True`, it will only print the jobs that would be cancelled.
    """
    jobs_to_cancel = get_running_here(user=user, folder=folder, prefix=prefix, sufix=sufix, key_jobid=key_jobid, get_files=False)
    if testing:
        print('The following jobs would be cancelled:')
        for job in jobs_to_cancel:
            print(f'{job}')
        return None
    for job in jobs_to_cancel:
        call.bash(f'scancel {job}', folder)
    return None


def get_running_here(
        user:str='',
        folder=None,
        prefix:str='slurm-',
        sufix:str='.out',
        key_jobid:str='JOBID',
        get_files=False
        ) -> list:
    """Return a list with all running `jobs` in a given `folder`, or current working directory if not specified.

    The jobs will be detected from the `<prefix>JOBID<sufix>` files, `slurm-JOBID.out` by default.

    If an `user` name is provided, it additionally checks if the jobs are actually scheduled
    to avoid reporting or killing jobs that have already finished.
    If the slurm squeue 'JOBID' title is different in your cluster,
    change it with `key_jobid`.

    If `get_files=True`, a list with the filenames will be returned instead of the JOBIDs.
    """
    filenames = file.get_list(folder=folder, include=prefix, abspath=False)
    if not filenames:
        raise FileNotFoundError(f'To detect the calculations, {prefix}JOBID{sufix} files are needed!\nConfigure the folder, as well as the prefix and sufix if necessary.')
    jobs = []
    for filename in filenames:
        filename = filename.replace(prefix, '')
        filename = filename.replace(sufix, '')
        jobs.append(filename)
    # Check if the jobs are actually scheduled
    if user:
        df = squeue(user)
        jobid_list = df[key_jobid].tolist()
        jobs = [job for job in jobs if job in jobid_list]
    # Return the filenames if specified
    if get_files:
        if user:
            filenames = [f for f in filenames if any(job in f for job in jobs)]
        return filenames
    return jobs


def check_template(
        template:str='template.slurm',
        folder=None,
    ) -> str:
    """Check the slurm `template` inside `folder`, to be used by `sbatch()`.

    The current working directory is used if `folder` is not provided.
    If the file does not exist or is invalid, creates a `template_EXAMPLE.slurm` file for reference.
    """
    folder = call.here(folder)
    slurm_example = 'template_EXAMPLE.slurm'
    new_slurm_file = os.path.join(folder, slurm_example)
    # Default slurm template
    content =f'''# Automatic slurm template created with ATON {__version__}\n# https://pablogila.github.io/ATON
#!/bin/bash
#SBATCH --partition=general
#SBATCH --qos=regular
#SBATCH --job-name=JOBNAME
#SBATCH --ntasks=32
#SBATCH --time=1-00:00:00
#SBATCH --mem=128G
# #SBATCH --mail-user=YOUR@EMAIL
# #SBATCH --mail-type=END

module purge
module load QuantumESPRESSO/7.3-foss-2023a

srun --cpu_bind=cores pw.x -inp INPUT > OUTPUT
'''
    # If the slurm template does not exist, create one
    slurm_file = file.get(folder, template, True)
    if not slurm_file:
        with open(new_slurm_file, 'w') as f:
            f.write(content)
        print(f'!!! WARNING:  Slurm template missing, an example was generated automatically:\n'
              f'{slurm_example}\n'
              f'PLEASE CHECK it, UPDATE it and RENAME it to {template}\n'
              'before using aton.api.slurm.sbatch()\n')
        return None
    # Check that the slurm file contains the INPUT_FILE, OUTPUT_FILE and JOB_NAME keywords
    key_input = find.lines(slurm_file, 'INPUT')
    key_output = find.lines(slurm_file, 'OUTPUT')
    key_jobname = find.lines(slurm_file, 'JOBNAME')
    missing = []
    if not key_input:
        missing.append('INPUT')
    if not key_output:
        missing.append('OUTPUT')
    if not key_jobname:
        missing.append('JOBNAME')
    if len(missing) > 0:
        with open(new_slurm_file, 'w') as f:
            f.write(content)
        print('!!! WARNING:  Some keywords were missing from your slurm template,\n'
              f'PLEASE CHECK the example at {slurm_example}\n'
              'before using aton.api.slurm.sbatch()\n'
              f'The following keywords were missing from your {template}:')
        for key in missing:
            print(key)
        print('')
        return None
    return slurm_file  # Ready to use!

