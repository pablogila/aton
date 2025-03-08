"""
# Description

Tools to work with the [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) module from [Quantum ESPRESSO](https://www.quantum-espresso.org/).  


# Index

Input and output reading  
`read_in()`  
`read_out()`  
`read_dir()`  
`read_dirs()`  

Input file manipulation  
`set_value()`  
`add_atom()`  
`scf_from_relax()`  

Data extraction  
`get_atom()`  
`count_elements()`  
`normalize_card()`  
`to_cartesian()`  
`from_cartesian()`  

Dicts with input file description  
`pw_namelists`  
`pw_cards`  

---
"""


import pandas as pd
import numpy as np
import os
from aton._version import __version__
import aton.file as file
import aton.phys.atoms
import aton.txt.find as find
import aton.txt.edit as edit
import aton.txt.extract as extract


def read_in(filepath) -> dict:
    """Reads a Quantum ESPRESSO input `filepath` and returns the values as a dict.

    Dict keys are named after the corresponding variable.
    CARDS are returned as lists, and contain the
    title card + parameters in the first item.
    """
    file_path = file.get(filepath)
    data = {}
    # First get the values from the namelists
    lines = find.lines(file_path, '=')
    for line in lines:
        line.strip()
        var, value = line.split('=', 1)
        var = var.strip()
        value = value.strip()
        if var.startswith('!'):
            continue
        try:
            value_float = value.replace('d', 'e')
            value_float = value_float.replace('D', 'e')
            value_float = value_float.replace('E', 'e')
            value_float = float(value_float)
            value = value_float
            if var in _pw_int_values: # Keep ints as int
                value = int(value)
        except ValueError:
            pass # Then it is a string
        data[var] = value
    # Try to find all the cards. Card titles will be saved in the 0 position of each result.
    for card in pw_cards.keys():
        card_lower = card.lower()
        card_uncommented = rf'(?!\s*!\s*)({card}|{card_lower})'
        card_content = find.between(filepath=file_path, key1=card_uncommented, key2=_all_cards_regex, include_keys=True, match=-1, regex=True)
        if not card_content:
            continue
        # If found, clean and normalise the card's content
        card_content = card_content.splitlines()
        card_content = normalize_card(card_content)
        data[card] = card_content
    # If there are CELL_PARAMETERS, check if we can extract the alat to celldm(1).
    if 'CELL_PARAMETERS' in data.keys():
        if 'alat' in data['CELL_PARAMETERS'][0]:
            alat = extract.number(data['CELL_PARAMETERS'][0])
            if alat:  # This overwrites any possible celldm(1) previously defined!
                data['celldm(1)'] = alat
                data['CELL_PARAMETERS'][0] = 'CELL_PARAMETERS alat'
    return data


def read_out(filepath) -> dict:
    """Reads a Quantum ESPRESSO output `filepath`, returns a dict with the output keys.

    The output keys are:
    `'Energy'` (Ry), `'Total force'` (float), `'Total SCF correction'` (float),
    `'Runtime'` (str), `'JOB DONE'` (bool), `'BFGS converged'` (bool), `'BFGS failed'` (bool),
    `'Maxiter reached'` (bool), `'Error'` (str), `'Success'` (bool), `'CELL_PARAMETERS_out'` (list of str), `'ATOMIC_POSITIONS_out'` (list of str), `'Alat'` (bohr), `'Volume'` (a.u.^3), `'Density'` (g/cm^3).

    Note that these output keys start with a **C**apital letter.
    """
    file_path = file.get(filepath)

    energy_key           = '!    total energy'
    force_key            = 'Total force'
    scf_key              = 'Total SCF correction'
    time_key             = 'PWSCF'
    time_stop_key        = 'CPU'
    job_done_key         = 'JOB DONE.'
    bfgs_converged_key   = 'bfgs converged'
    bfgs_failed_key      = 'bfgs failed'
    maxiter_reached_key  = 'Maximum number of iterations reached'
    error_key            = 'Error in routine'
    error_failed_line    = 'pw.x: Failed'
    cell_parameters_key  = 'CELL_PARAMETERS'
    atomic_positions_key = 'ATOMIC_POSITIONS'

    energy_line          = find.lines(file_path, energy_key, -1)
    force_line           = find.lines(file_path, force_key, -1)
    time_line            = find.lines(file_path, time_key, -1)
    job_done_line        = find.lines(file_path, job_done_key, -1)
    bfgs_converged_line  = find.lines(file_path, bfgs_converged_key, -1)
    bfgs_failed_line     = find.lines(file_path, bfgs_failed_key, -1)
    maxiter_reached_line = find.lines(file_path, maxiter_reached_key, -1)
    error_line           = find.lines(file_path, error_key, -1, 1, True)
    error_failed_line    = find.lines(file_path, error_failed_line, -1)

    energy: float = None
    force: float = None
    scf: float = None
    time: str = None
    job_done: bool = False
    bfgs_converged: bool = False
    bfgs_failed: bool = False
    maxiter_reached: bool = False
    error: str = ''
    success: bool = False

    if energy_line:
        energy = extract.number(energy_line[0], energy_key)
    if force_line:
        force = extract.number(force_line[0], force_key)
        scf = extract.number(force_line[0], scf_key)
    if time_line:
        time = extract.string(time_line[0], time_key, time_stop_key)
    if job_done_line:
        job_done = True
    if bfgs_converged_line:
        bfgs_converged = True
    if bfgs_failed_line:
        bfgs_failed = True
    if maxiter_reached_line:
        maxiter_reached = True
    if error_line:
        error = error_line[1].strip()
    elif error_failed_line:
        error = error_failed_line[0].strip()
    
    # Was the calculation successful?
    if job_done and not bfgs_failed and not maxiter_reached and not error:
        success = True

    # CELL_PARAMETERS and ATOMIC_POSITIONS
    cell_parameters = None
    atomic_positions = None
    alat = None
    volume = None
    density = None
    coordinates_raw = find.between(file_path, 'Begin final coordinates', 'End final coordinates', False, -1, False)
    if coordinates_raw:
        coordinates_raw = coordinates_raw.splitlines()
        append_cell = False
        append_positions = False
        cell_parameters_raw = []
        atomic_positions_raw = []
        for line in coordinates_raw:
            line = line.strip()
            if cell_parameters_key in line:
                append_cell = True
                append_positions = False
            elif atomic_positions_key in line:
                append_cell = False
                append_positions = True
            elif 'volume' in line:
                volume = extract.number(line, 'volume')
            elif 'density' in line:
                density = extract.number(line, 'density')
            if line == '' or line.startswith('!'):
                continue
            if append_cell:
                cell_parameters_raw.append(line)
            elif append_positions:
                atomic_positions_raw.append(line)
        cell_parameters = normalize_card(cell_parameters_raw)
        atomic_positions = normalize_card(atomic_positions_raw)
        if cell_parameters:
            if 'alat' in cell_parameters[0]:
                alat = extract.number(cell_parameters[0], 'alat')

    output = {
        'Energy'                : energy,
        'Total force'           : force,
        'Total SCF correction'  : scf,
        'Runtime'               : time,
        'JOB DONE'              : job_done,
        'BFGS converged'        : bfgs_converged,
        'BFGS failed'           : bfgs_failed,
        'Maxiter reached'       : maxiter_reached,
        'Error'                 : error,
        'Success'               : success,
        'CELL_PARAMETERS_out'   : cell_parameters,
        'ATOMIC_POSITIONS_out'  : atomic_positions,
        'Alat'                  : alat,
        'Volume'                : volume,
        'Density'               : density,
    }
    return output


def read_dir(
        folder,
        in_str:str='.in',
        out_str:str='.out'
    ) -> dict:
    """Takes a `folder` from a QE calculation, returns a dict with input and output values.
    
    Input and output files are determined automatically,
    but must be specified with `in_str` and `out_str`
    if more than one file ends with `.in` or `.out`.
    """
    input_file = file.get(folder, in_str)
    output_file = file.get(folder, out_str)
    if not input_file and not output_file:
        return None
    if input_file:
        dict_in = read_in(input_file)
        if not output_file:
            return dict_in
    if output_file:
        dict_out = read_out(output_file)
        if not input_file:
            return dict_out
    # Merge both dictionaries
    merged_dict = {**dict_in, **dict_out}
    return merged_dict


def read_dirs(
        directory,
        in_str:str='.in',
        out_str:str='.out',
        calc_splitter='_',
        calc_type_index=0,
        calc_id_index=1
    ) -> None:
    """Reads recursively QE calculations from all the subfolders inside the given `directory`.

    Results are saved to CSV files inside the current directory.
    Input and output files are determined automatically, but must be specified with
    `in_str` and `out_str` if more than one file ends with `.in` or `.out`.

    To properly group the calculations per type, saving separated CSVs for each calculation type,
    you can modify `calc_splitter` ('_' by default), `calc_type_index` (0) and `calc_id_index` (1).
    With these default values, a subfolder named './CalculationType_CalculationID_AdditionalText/'
    will be interpreted as follows:
    - Calculation type: 'CalculationType' (The output CSV will be named after this)
    - CalculationID: 'CalculationID' (Stored in the 'ID' column of the resulting dataframe)

    If everything fails, the subfolder name will be used for the CSV file.
    """
    print(f'Reading all Quantum ESPRESSO calculations from {directory} ...')
    folders = file.get_list(directory)
    if not folders:
        raise FileNotFoundError('The directory is empty!')
    # Separate calculations by their title in an array
    calc_types = []
    folders.sort()
    for folder in folders:
        if not os.path.isdir(folder):
            folders.remove(folder)
            continue
        folder_name = os.path.basename(folder)
        try:
            calc_name = folder_name.split(calc_splitter)[calc_type_index]
        except:
            calc_name = folder_name
        if not calc_name in calc_types:
            calc_types.append(calc_name)
    len_folders = len(folders)
    total_success_counter = 0
    for calc in calc_types:
        len_calcs = 0
        success_counter = 0
        results = pd.DataFrame()
        for folder in folders:
            if not calc in folder:
                continue
            len_calcs += 1
            folder_name = os.path.basename(folder)
            try:
                calc_id = folder_name.split(calc_splitter)[calc_id_index]
            except:
                calc_id = folder_name
            df = pd.DataFrame.from_dict(read_dir(folder, in_str, out_str))
            if df is None:
                continue
            # Join input and output in the same dataframe
            df.insert(0, 'ID', calc_id)
            df = df.dropna(axis=1, how='all')
            results = pd.concat([results, df], axis=0, ignore_index=True)
            if df['Success'][0]:
                success_counter += 1
                total_success_counter += 1
        results.to_csv(os.path.join(directory, calc+'.csv'))
        print(f'Saved to CSV: {calc} ({success_counter} successful calculations out of {len_calcs})')
    print(f'Total successful calculations: {total_success_counter} out of {len_folders}')


def set_value(
        filepath,
        key:str,
        value,
        indent:str='  ',
    ) -> None:
    """Replace the `value` of a `key` parameter in an input `filepath`.
    
    Delete parameters with `value=''`.
    Remember to include the single quotes `'` on values that use them.

    Updating 'ATOMIC_POSITIONS' updates 'nat' automatically,
    and updating 'ATOMIC_SPECIES' updates 'ntyp'.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    key = key.strip()
    file_path = file.get(filepath)
    input_old = read_in(file_path)
    # Present keys uppercase
    present_keys_upper = []
    for present_key in input_old.keys():
        present_keys_upper.append(present_key.upper())
    # All namelist values
    pw_values = []
    for namelist_values in pw_namelists.values():
        pw_values.extend(namelist_values)
    # All cards
    pw_cards_upper = []  # Don't forget about these!
    for card in pw_cards.keys():
        pw_cards_upper.append(card.upper())
    # Check if it's a namelist
    if key in pw_values:
        if key in input_old.keys():
            _update_value(filepath, key, value, indent)
        else:  # Write the value from scratch
            _add_value(filepath, key, value, indent)
    # Check if it's a card
    elif key.upper() in pw_cards_upper:
        if key.upper() in present_keys_upper:
            _update_card(filepath, key, value, indent)
        else:
            _add_card(filepath, key, value, indent)
    else:
        raise ValueError(f'Unrecognised key: {key}')
    return None


def _update_value(
        filepath,
        key:str,
        value,
        indent:str='  '
        ) -> None:
    """Update the `value` of an existing `key` from a namelist. Called by `set_value()`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    key = key.strip()
    key_uncommented = key
    key_uncommented = key_uncommented.replace('(', r'\(')
    key_uncommented = key_uncommented.replace(')', r'\)')
    key_uncommented = rf'(?!\s*!\s*){key_uncommented}'
    # Convert to int if necessary
    if key in _pw_int_values:
        value = int(value)
    line = f'{indent}{key} = {value}'
    if value == '':
        line = ''
    edit.replace_line(filepath=filepath, key=key_uncommented, text=line, replacements=1, regex=True)
    _update_other_values(filepath, key, value, indent)
    return None


def _add_value(
        filepath,
        key:str,
        value,
        indent:str='  '
    ) -> None:
    """Adds a `key` = `value` to a NAMELIST. Called by `set_value()`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    if value == '':  # No need to delete an unexisting value!
        return None
    if key in _pw_int_values:
        value = int(value)
    key = key.strip()
    value = str(value).strip()
    # Which namelist?
    parent_namelist = None
    for namelist in pw_namelists.keys():
        if key in pw_namelists[namelist]:
            parent_namelist = namelist
            break
    if not parent_namelist:
        raise ValueError(f"Key is not valid, '{key}' is not from any NAMELIST!")
    # Add the parent namelist if it does not exist, then add the value
    _add_namelist(filepath, parent_namelist)
    # Convert to int if necessary
    if value in _pw_int_values:
        value = int(value)
    line = f'{indent}{key} = {value}'
    parent_namelist_regex = rf'(?!\s*!\s*)({parent_namelist}|{parent_namelist.lower()})'
    edit.insert_under(filepath=filepath, key=parent_namelist_regex, text=line, insertions=1, regex=True)
    # Update other values if necessary
    _update_other_values(filepath, key, value, indent)
    return None


def _add_namelist(
        filepath,
        namelist:str,
    ) -> None:
    """Adds a `namelist` to the `filepath` if not present. Called by `add_value()` if needed."""
    namelists = list(pw_namelists.keys())
    namelist = namelist.upper().strip()
    if not namelist in namelists:
        raise ValueError(f'{namelist} is not a valid namelist! Valid namelists are:\n{namelists}')
    # Is the namelist already there?
    namelist_regex = rf'(?!\s*!\s*)({namelist}|{namelist.lower()})'
    is_present = find.lines(filepath=filepath, key=namelist_regex, regex=True)
    if is_present:
        return None
    # Find where to insert the namelist, from last to first.
    # We might have to insert it on top of the first CARD found.
    next_namelist =  _all_cards_regex
    namelists.reverse()
    # Get the present namelists, plus the target one
    present_namelists = []
    for section in namelists:
        is_section_present = find.lines(filepath=filepath, key=rf'(?!\s*!\s*)({section})', regex=True)
        if is_section_present or section.upper() == namelist.upper():
            present_namelists.append(section)
    # Get the very next section after the desired one
    for section in present_namelists:
        if section == namelist:
            break
        next_namelist = rf'(?!\s*!\s*)({section})(?!\s*=)'
    # Insert the target namelist on top of it!
    edit.insert_under(filepath, next_namelist, f'{namelist}\n/\n', 1, -1, True)
    return None


def _update_card(
        filepath,
        key:str,
        value:list,
        indent:str='  ',
    ) -> None:
    """Updates the `value` of a `key` CARD, present in `filepath`. Called by `set_value()`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    if value == '':
        return None
    value = normalize_card(value, indent)
    # Replace the CARD value up to the next CARD found
    key = key.upper().strip()
    key_uncommented = rf'(?!\s*!\s*)({key}|{key.lower()})'
    lines = '\n'.join(value)
    edit.replace_between(filepath=filepath, key1=key_uncommented, key2=_all_cards_regex, text=lines, delete_keys=False, regex=True)
    # We added the CARD below the previous CARD title, so we remove the previous CARD title
    edit.replace_line(filepath, key_uncommented, '', 1, 0, 0, True)
    # We might have to update other values, such as nat or ntyp
    _update_other_values(filepath, key, value, indent)
    return None


def _add_card(
        filepath,
        key:str,
        value:list,
        indent:str='  '
    ) -> None:
    """Adds a non-present `key` CARD with a given `value` to the `filepath`. Called by `set_value()`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    if value == '':
        return None
    value = normalize_card(value, indent)
    insert_value = value
    if isinstance(value, list):
        insert_value = '\n'.join(value)
    edit.insert_at(filepath, insert_value, -1)
    _update_other_values(filepath, key, value, indent)
    return None


def _update_other_values(
        filepath,
        key:str,
        value,
        indent:str='  '
    ) -> None:
    """Updates values that depend on the input value, eg. updates 'nat' when updating ATOMIC_POSITIONS.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    file_path = file.get(filepath)
    old_values = read_in(file_path)
    # Key in upper cases for CARD values
    key = key.strip().upper()
    # CELL_PARAMETERS ?
    if key in ['CELL_PARAMETERS', 'CELL_PARAMETERS_OUT']:
        if 'angstrom' in value[0] or 'bohr' in value[0]:
            edit.replace_line(file_path, r'(?!\s*!\s*)celldm\(\d\)\s*=', '', 1, 0, 0, True)
            edit.replace_line(file_path, r'(?!\s*!\s*)[ABC]\s*=', '', 1, 0, 0, True)
            edit.replace_line(file_path, r'(?!\s*!\s*)cos[AB][BC]\s*=', '', 1, 0, 0, True)
        elif 'alat' in value[0]:
            alat = extract.number(value[0])
            if alat:
                edit.replace_line(file_path, r'(?!\s*!\s*)CELL_PARAMETERS', 'CELL_PARAMETERS alat', -1, 0, 0, True)
                edit.replace_line(file_path, r'(?!\s*!\s*)celldm\(\d\)\s*=', f'celldm(1) = {alat}', 1, 0, 0, True)
        return None
    # ATOMIC_SPECIES ?
    elif key == 'ATOMIC_SPECIES':
        old_ntyp = old_values['ntyp']
        elements_found = []
        for line in value[1:]:
            element = extract.element(line)
            if element:
                if not element in elements_found:
                    elements_found.append(element)
        new_ntyp = len(elements_found)
        if old_ntyp != new_ntyp:
            set_value(filepath, 'ntyp', new_ntyp, indent)
        return None
    # ATOMIC_POSITIONS ?
    elif key in ['ATOMIC_POSITIONS', 'ATOMIC_POSITIONS_OUT']:
        new_nat = len(value) - 1
        if old_values['nat'] != new_nat:
            set_value(filepath, 'nat', new_nat, indent)
        return None
    # Key in lower case for NAMELIST values
    key = key.lower()
    # Lattice params Angstroms?
    if key in ['a', 'b', 'c', 'cosab', 'cosac', 'cosbc']:
        edit.replace_line(file_path, r'(?!\s*!\s*)celldm\(\d\)\s*=', '', 1, 0, 0, True)
        edit.replace_line(file_path, r'(?!\s*!\s*)CELL_PARAMETERS', 'CELL_PARAMETERS alat', -1, 0, 0, True)
        return None
    # Lattice params Bohrs ?
    elif 'celldm(' in key:
        edit.replace_line(file_path, r'(?!\s*!\s*)[ABC]\s*=', '', 1, 0, 0, True)
        edit.replace_line(file_path, r'(?!\s*!\s*)cos[AB][BC]\s*=', '', 1, 0, 0, True)
        edit.replace_line(file_path, r'(?!\s*!\s*)CELL_PARAMETERS', 'CELL_PARAMETERS alat', -1, 0, 0, True)
        return None
    return None


def add_atom(filepath, position, indent='  ') -> None:
    """Adds an atom in a given input `filepath` at a specified `position`.

    Position must be a string or a list, as follows:
    `"specie:str float float float"` or `[specie:str, float, float, float]`.

    This method updates automatically other related values,
    such as 'ntyp' when updating ATOMIC_SPECIES, etc.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    new_atom = position
    if isinstance(position, list):
        if not len(position) == 4 or not isinstance(position[0], str):
            raise ValueError('If your atomic position is a list, it must contain the atom type and the three coords, as in [str, str/float, str/float, str/float]')
        new_atom = '   '.join(str(x) for x in position)
    elif not isinstance(position, str):
        raise ValueError(f'The specified position must be a list of size 4 (atom type and three coordinates) or an equivalent string! Your position was:\n{coords}')
    # Let's check that our new_atom makes sense
    atom = extract.element(new_atom)
    coords = extract.coords(new_atom)
    if not atom:
        raise ValueError(f'The specified position does not contain an atom at the beginning! Your position was:\n{position}')
    if len(coords) < 3:
        raise ValueError(f'Your position has len(coordinates) < 3, please check it.\nYour position was: {position}\nCoordinates detected: {coords}')
    if len(coords) > 3:
        coords = coords[:3]
    new_atom = f'{atom}   {coords[0]}   {coords[1]}   {coords[2]}'
    # Get the values from the file
    values = read_in(filepath)
    atomic_positions = values['ATOMIC_POSITIONS']
    atomic_positions.append(new_atom)
    # Update ATOMIC_POSITIONS. nat should be updated automatically.
    set_value(filepath=filepath, key='ATOMIC_POSITIONS', value=atomic_positions, indent=indent)
    # We might have to update ATOMIC_SPECIES!
    atomic_species = values['ATOMIC_SPECIES']
    is_atom_missing = True
    for specie in atomic_species[1:]:
        if atom == extract.element(specie):
            is_atom_missing = False
            break
    if is_atom_missing:  # Update ATOMIC_SPECIES. ntyp should be updated automatically.
        mass = aton.phys.atoms[atom].mass
        atomic_species.append(f'{atom}   {mass}   {atom}.upf')
        set_value(filepath=filepath, key='ATOMIC_SPECIES', value=atomic_species, indent=indent)
    return None


def get_atom(
        filepath:str,
        position:list,
        precision:int=3,
        return_anyway:bool=False,
    ) -> str:
    """Takes the approximate `position` of an atom, and returns the full line from the input `filepath`.

    It compares the atomic positions rounded up to the specified `precision` decimals.
    If `return_anyway = True`, ignores errors and returns an empty string.
    """
    # Check that the coordinates are valid
    if isinstance(position, str):
        coordinates = extract.coords(position)
    elif isinstance(position, list):
        coordinates = position
        if len(position) == 1 and isinstance(position[0], str):  # In case someone like me introduces ['x, y, z']
            coordinates = extract.coords(position[0])
    else:
        if return_anyway:
            return ''
        raise ValueError(f'The atomic position must be a list or a string! Yours was:\n{position}\nDetected coordinates:\n{coordinates}')
    if len(coordinates) < 3:
        if return_anyway:
            return ''
        raise ValueError(f'Atomic position has less that 3 coordinates! Yours had len={len(coordinates)}:\n{position}\nDetected coordinates:\n{coordinates}')
    if len(coordinates) > 3:
        coordinates = coordinates[:3]
    # Round the input position up to the specified precision
    coordinates_rounded = []
    for coordinate in coordinates:
        coordinates_rounded.append(round(coordinate, precision))
    # Compare the rounded coordinates with the atomic positions
    content = read_in(filepath)
    if not 'ATOMIC_POSITIONS' in content.keys():
        if return_anyway:
            return ''
        raise ValueError(f'ATOMIC_POSITIONS missing in {filepath}')
    atomic_positions = content['ATOMIC_POSITIONS'][1:]  # Remove header
    matched_pos = None
    matched_index = None
    for i, atomic_position in enumerate(atomic_positions):
        coords =  extract.coords(atomic_position)
        coords_rounded = []
        for pos in coords:
            coords_rounded.append(round(pos, precision))
        if coordinates_rounded == coords_rounded:
            if matched_pos: # There was a previous match!
                if return_anyway:
                    return ''
                raise ValueError(f'More than one matching position found! Try again with more precision.\nSearched coordinates: {coordinates_rounded}')
            matched_pos = atomic_position
            matched_index = i
    if not matched_pos:
        if return_anyway:
            return ''
        raise ValueError(f'No matching position found! Try again with a less tight precision parameter.\nSearched coordinates: {coordinates_rounded}')
    # We must get the literal line, not the normalized one!
    atomic_positions_uncommented = rf'(?!\s*!\s*)(ATOMIC_POSITIONS|atomic_positions)'
    atomic_positions_lines = find.between(filepath=filepath, key1=atomic_positions_uncommented, key2=_all_cards_regex, include_keys=False, match=-1, regex=True)
    # Remove commented or empty lines
    atomic_positions_lines = atomic_positions_lines.splitlines()
    atomic_positions_cleaned = []
    for line in atomic_positions_lines:
        if line == '' or line.startswith('!') or line.startswith('#'):
            continue
        atomic_positions_cleaned.append(line)
    matched_line = atomic_positions_cleaned[matched_index]
    return matched_line.strip()


def normalize_card(card:list, indent='') -> list:
    """Take a matched card, and return it in a normalised format.

    Optionally change indentation with `indent`, 0 spaces by default.
    """
    # Make sure it is a list!
    if isinstance(card, str):
        card = card.split('\n')
    if not isinstance(card, list):
        raise ValueError(f"Card must be a string or a list of strings! Yours was:\n{card}")
    # Keep the header
    cleaned_content = [card[0].strip()]
    for line in card[1:]:
        line = line.strip()
        if line == '' or line.startswith('!') or line.startswith('#'):
            continue
        elif any(key in line.upper() for key in pw_cards.keys()):
            break
        items = line.split()
        cleaned_line = f'{indent}{items[0].strip()}'  # Add the specified intent at the start of the line
        for item in items[1:]:
            item = item.strip()
            cleaned_line = cleaned_line + '   ' + item  # Three spaces between elements
        cleaned_content.append(cleaned_line)
    # Perform extra normalization for some CARDs
    if any(key in cleaned_content[0] for key in ['cell_parameters', 'CELL_PARAMETERS']):
        cleaned_content = _normalize_cell_parameters(cleaned_content, indent)
    elif any(key in cleaned_content[0] for key in ['atomic_positions', 'ATOMIC_POSITIONS']):
        cleaned_content = _normalize_atomic_positions(cleaned_content, indent)
    elif any(key in cleaned_content[0] for key in ['atomic_species', 'ATOMIC_SPECIES']):
        cleaned_content = _normalize_atomic_species(cleaned_content, indent)
    elif any(key in cleaned_content[0] for key in ['k_points', 'K_POINTS']):
        cleaned_content = _normalize_k_points(cleaned_content)
    return cleaned_content


def _normalize_cell_parameters(card, indent='') -> list:
    """Performs extra formatting to a previously cleaned CELL_PARAMETERS `card`.

    Optionally change indentation with `indent`, 0 spaces by default.
    """
    if card == None:
        return None
    cell_parameters = [card[0].strip()]
    for line in card[1:]:
        coords = extract.coords(line)
        if len(coords) < 3:
            raise ValueError(f'Each CELL_PARAMETER must have three coordinates! Yours was:\n{card}\nDetected coordinates were:\n{coords}')
        if len(coords) > 3:  # This should never happen but who knows...
            coords = coords[:3]
        new_line = f"{indent}{coords[0]:.15f}   {coords[1]:.15f}   {coords[2]:.15f}"
        cell_parameters.append(new_line)
    # Normalise the header
    if 'angstrom' in cell_parameters[0]:
        cell_parameters[0] = 'CELL_PARAMETERS angstrom'
    elif 'bohr' in cell_parameters[0]:
        cell_parameters[0] = 'CELL_PARAMETERS bohr'
    elif 'alat' in cell_parameters[0]:
        alat = extract.number(cell_parameters[0], 'alat')
        if alat:
            cell_parameters[0] = f'CELL_PARAMETERS alat= {alat}'
        else:
            cell_parameters[0] = 'CELL_PARAMETERS alat'
    else:
        raise ValueError(f'CELL_PARAMETERS must contain angstrom, bohr or alat! Yours was:\n{cell_parameters}')
    return cell_parameters


def _normalize_atomic_positions(card, indent='') -> list:
    """Performs extra formatting to a previously cleaned ATOMIC_POSITIONS `card`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    if card == None:
        return None
    atomic_positions = [card[0].strip()]
    for line in card[1:]:
        line = line.strip()
        atom = extract.element(line)
        if not atom:
            raise ValueError(f'Atoms must be defined as the atom (H, He, Na...) or the isotope (H2, He4...)! Yours was:\n{line}')
        coords = extract.coords(line)
        if len(coords) < 3:
            raise ValueError(f'Each ATOMIC_POSITION must have at least three coordinates! Yours contained the line:\n{line}\nDetected coordinates were:\n{coords}')
        if len(coords) > 6:  # Including optional parameters
            coords = coords[:6]
        new_line = f"{indent}{atom}"
        for coord in coords:
            new_line = f"{new_line}   {coord:.15f}"
        atomic_positions.append(new_line)
    if 'alat' in atomic_positions[0]:
        atomic_positions[0] = 'ATOMIC_POSITIONS alat'
    elif 'bohr' in atomic_positions[0]:
        atomic_positions[0] = 'ATOMIC_POSITIONS bohr'
    elif 'angstrom' in atomic_positions[0]:
        atomic_positions[0] = 'ATOMIC_POSITIONS angstrom'
    elif 'crystal_sg' in atomic_positions[0]:
        atomic_positions[0] = 'ATOMIC_POSITIONS crystal_sg'
    elif 'crystal' in atomic_positions[0]:
        atomic_positions[0] = 'ATOMIC_POSITIONS crystal'
    else:
        raise ValueError(f"ATOMIC_POSITIONS[0] must contain alat, bohr, angstrom, crystal or crystal_sg. Yours was:\n{atomic_positions[0]}")
    return atomic_positions


def _normalize_atomic_species(card, indent='') -> list:
    """Performs extra formatting to a previously cleaned ATOMIC_SPECIES `card`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    if card == None:
        return None
    atomic_species = [card[0].strip()]
    for line in card[1:]:
        line = line.strip()
        atom = extract.element(line)
        if not atom:
            raise ValueError(f'Atom must be specified at the beginning! Your line was:\n{line}')
        mass_list = extract.coords(line)
        if len(mass_list) == 1:
            mass = mass_list[0]
        else:  # Is the mass missing?
            raise ValueError(f'Mass is not properly specified: {line}')
        # Get the pseudo in the third position
        line_split = line.split()
        if len(line_split) < 3:
            raise ValueError(f'Does the ATOMIC_SPECIES contain the pseudopotential? Your line was:\n{line}')
        pseudopotential = line_split[2]
        full_line = f"{indent}{atom}   {mass}   {pseudopotential}"
        atomic_species.append(full_line)
    return atomic_species


def _normalize_k_points(card, indent='') -> list:
    """Performs extra formatting to a previously cleaned K_POINTS `card`.

    Optionally change indentation with `indent`, 2 spaces by default.
    """
    if card == None:
        return None
    k_points = [card[0].strip()]
    points = card[1].split()
    line = f'{indent}{points[0].strip()}'
    for point in points[1:]:
        line = f'{line} {point.strip()}'
    k_points.append(line)
    if 'automatic' in k_points[0]:
        k_points[0] = 'K_POINTS automatic'
    elif 'gamma' in k_points[0]:
        k_points[0] = 'K_POINTS gamma'
    elif 'tpiba_b' in k_points[0]:
        k_points[0] = 'K_POINTS tpiba_b'
    elif 'tpiba_c' in k_points[0]:
        k_points[0] = 'K_POINTS tpiba_c'
    elif 'tpiba' in k_points[0]:
        k_points[0] = 'K_POINTS tpiba'
    elif 'crystal_b' in k_points[0]:
        k_points[0] = 'K_POINTS crystal_b'
    elif 'crystal_c' in k_points[0]:
        k_points[0] = 'K_POINTS crystal_c'
    elif 'crystal' in k_points[0]:
        k_points[0] = 'K_POINTS crystal'
    else:
        raise ValueError(f'K_POINTS must be tpiba, automatic, crystal, gamma, tpiba_b, crystal_b, tpiba_c, or crystal_c. Yours was:\n{k_points}')
    return k_points


def count_elements(atomic_positions) -> dict:
    """Takes ATOMIC_POSITIONS, returns a dict as `{element : number of atoms}`"""
    if isinstance(atomic_positions, str):
        atomic_positions.split()
    if not isinstance(atomic_positions, list):
        raise ValueError(f'To count the elements, atomic_positions must be a list or a str! Yours was:\n{atomic_positions}')
    elements = {}
    if any(header in atomic_positions[0] for header in ['ATOMIC_POSITIONS', 'atomic_positions']):
        atomic_positions = atomic_positions[1:]
    for line in atomic_positions:
        element = extract.element(line)
        if not element:
            continue
        if element in elements.keys():
            elements[element] = elements[element] + 1
        else:
            elements[element] = 1
    return elements


def scf_from_relax(
        folder:str=None,
        relax_in:str='relax.in',
        relax_out:str='relax.out'
    ) -> None:
    """Create a Quantum ESPRESSO `scf.in` file from a previous relax calculation.
    
    If no `folder` is provided, the current working directory is used.
    The `relax_in` and `relax_out` files by default are `relax.in` and `relax.out`,
    update the names if necessary.
    """
    # Terminal feedback
    print(f'\naton.interface.qe {__version__}\n'
          f'Creating Quantum ESPRESSO SCF input from previous relax calculation:\n'
          f'{relax_in}\n{relax_out}\n')
    folder_path = folder
    if not folder_path:
        folder_path = os.getcwd()
    relax_in = file.get(folder_path, relax_in)
    relax_out = file.get(folder_path, relax_out)
    data = read_dir(folder_path, relax_in, relax_out)
    # Create the scf.in from the previous relax.in
    scf_in = os.path.join(folder_path, 'scf.in')
    comment = f'! Automatic SCF input made with aton.interface.qe {__version__}. https://github.com/pablogila/ThotPy'
    edit.from_template(relax_in, scf_in, None, comment)
    scf_in = file.get(folder_path, scf_in)
    # Replace CELL_PARAMETERS, ATOMIC_POSITIONS, ATOMIC_SPECIES, alat, ibrav and calculation
    atomic_species = data['ATOMIC_SPECIES']
    cell_parameters = data['CELL_PARAMETERS_out']
    atomic_positions = data['ATOMIC_POSITIONS_out']
    alat = data['Alat']
    set_value(scf_in, 'ATOMIC_SPECIES', atomic_species)
    set_value(scf_in, 'CELL_PARAMETERS', cell_parameters)
    set_value(scf_in, 'ATOMIC_POSITIONS', atomic_positions)
    set_value(scf_in, 'celldm(1)', alat)
    set_value(scf_in, 'ibrav', 0)
    set_value(scf_in, 'calculation', "'scf'")
    # Terminal feedback
    print(f'Created input SCF file at:'
          f'{scf_in}\n')
    return None


def to_cartesian(filepath, coordinates) -> str:
    """Converts a given `cordinates` from crystal lattice vectors to cartesian.

    Only for `ibrav=0`. Uses the cell parameters from the input `filepath`.
    Note that the result is not multiplied by `A` nor `celldm(1)`.
    """
    #print(f'COORDINATES: {coordinates}')
    cell_base = _get_base_change_matrix(filepath)
    coords = _clean_coords(coordinates)
    coords = np.array(coords).transpose()
    converted_coords = np.matmul(cell_base, coords)
    converted_coords_row = converted_coords.transpose()
    final_coords = converted_coords_row.tolist()
    #print(f'FINAL_COORDINATES: {final_coords}')
    return final_coords


def from_cartesian(filepath, coordinates:list) -> str:
    """Converts a given `cordinates` from cartesian to the base of lattice vectors.

    Only for `ibrav=0`. Uses the cell parameters from the input `filepath`.
    Note that the result is not divided by `A` nor `celldm(1)`.
    """
    #print(f'COORDINATES: {coordinates}')  # DEBUG
    cell_base = _get_base_change_matrix(filepath)
    cell_base_inverse = np.linalg.inv(cell_base)
    coords = _clean_coords(coordinates)
    coords = np.array(coords).transpose()
    converted_coords = np.matmul(cell_base_inverse, coords)
    converted_coords_row = converted_coords.transpose()
    final_coords = converted_coords_row.tolist()
    #print(f'FINAL_COORDINATES: {final_coords}')  # DEBUG
    return final_coords


def _get_base_change_matrix(filepath):
    """Get the base change matrix, based on the cell parameters. Only for `ibrav=0`."""
    content = read_in(filepath)
    # Get the base change matrix
    cell_parameters = content['CELL_PARAMETERS']
    cell_parameters = cell_parameters[1:]  # Remove header
    cell_coords = []
    for parameter in cell_parameters:
        #print(parameter)  # DEBUG
        coords = extract.coords(parameter)
        cell_coords.append(coords)
    cell_numpy = np.array(cell_coords)
    cell_base = cell_numpy.transpose()
    #print(f'BASE CHANGE MATRIX: {cell_base}')  # DEBUG
    return cell_base


def _clean_coords(coordinates) -> list:
    """Make sure that `coordinates` is a list with 3 floats. Removes extra values if present."""
    if isinstance(coordinates, str):
        coordinates = extract.coords(coordinates)
    if not isinstance(coordinates, list):
        raise ValueError("The coordinates must be a list of three floats, or a string as in 'Element x1 x2 x3'")
    if len(coordinates) < 3:
        raise ValueError("The coordinates must be a list of three floats, or a string as in 'Element x1 x2 x3'")
    if len(coordinates) > 3:
        coordinates = coordinates [:3]
    cleaned_coords = []
    for coord in coordinates:
        cleaned_coords.append(float(coord))
    return cleaned_coords


############################################################
####################  COMMON VARIABLES  ####################
############################################################


pw_namelists = {
    '&CONTROL' : ['calculation', 'title', 'verbosity', 'restart_mode', 'wf_collect', 'nstep', 'iprint', 'tstress', 'tprnfor', 'dt', 'outdir', 'wfcdir', 'prefix', 'lkpoint_dir', 'max_seconds', 'etot_conv_thr', 'forc_conv_thr', 'disk_io', 'pseudo_dir', 'tefield', 'dipfield', 'lelfield', 'nberrycyc', 'lorbm', 'lberry', 'gdir', 'nppstr', 'gate', 'twochem', 'lfcp', 'trism'],
    #
    '&SYSTEM' : ['ibrav', 'celldm(1)', 'celldm(2)', 'celldm(3)', 'celldm(4)', 'celldm(5)', 'celldm(6)', 'A', 'B', 'C', 'cosAB', 'cosAC', 'cosBC', 'nat', 'ntyp', 'nbnd', 'nbnd_cond', 'tot_charge', 'starting_charge', 'tot_magnetization', 'starting_magnetization', 'ecutwfc', 'ecutrho', 'ecutfock', 'nr1', 'nr2', 'nr3', 'nr1s', 'nr2s', 'nr3s', 'nosym', 'nosym_evc', 'noinv', 'no_t_rev', 'force_symmorphic', 'use_all_frac', 'occupations', 'one_atom_occupations', 'starting_spin_angle', 'degauss_cond', 'nelec_cond', 'degauss', 'smearing', 'nspin', 'sic_gamma', 'pol_type', 'sic_energy', 'sci_vb', 'sci_cb', 'noncolin', 'ecfixed', 'qcutz', 'q2sigma', 'input_dft', 'ace', 'exx_fraction', 'screening_parameter', 'exxdiv_treatment', 'x_gamma_extrapolation', 'ecutvcut' 'nqx1', 'nqx2', 'nqx3', 'localization_thr', 'Hubbard_occ', 'Hubbard_alpha', 'Hubbard_beta', 'starting_ns_eigenvalue', 'dmft', 'dmft_prefix', 'ensemble_energies', 'edir', 'emaxpos', 'eopreg', 'eamp', 'angle1', 'angle2', 'lforcet', 'constrained_magnetization', 'fixed_magnetization', 'lambda', 'report', 'lspinorb', 'assume_isolated', 'esm_bc', 'esm_w', 'esm_efield', 'esm_nfit', 'lgcscf', 'gcscf_mu', 'gcscf_conv_thr', 'gcscf_beta', 'vdw_corr', 'london', 'london_s6', 'london_c6', 'london_rvdw', 'london_rcut', 'dftd3_version', 'dftd3_threebody', 'ts_vdw_econv_thr', 'ts_vdw_isolated', 'xdm', 'xdm_a1', 'xdm_a2', 'space_group', 'uniqueb', 'origin_choice', 'rhombohedral', 'zgate', 'relaxz', 'block', 'block_1', 'block_2', 'block_height', 'nextffield'],
    #
    '&ELECTRONS' : ['electron_maxstep', 'exx_maxstep', 'scf_must_converge', 'conv_thr', 'adaptive_thr', 'conv_thr_init', 'conv_thr_multi', 'mixing_mode', 'mixing_beta', 'mixing_ndim', 'mixing_fixed_ns', 'diagonalization', 'diago_thr_init', 'diago_cg_maxiter', 'diago_ppcg_maxiter', 'diago_david_ndim', 'diago_rmm_ndim', 'diago_rmm_conv', 'diago_gs_nblock', 'diago_full_acc', 'efield', 'efield_cart', 'efield_phase', 'startingpot', 'startingwfc', 'tqr', 'real_space'],
    #
    '&IONS' : ['ion_positions', 'ion_velocities', 'ion_dynamics', 'pot_extrapolation', 'wfc_extrapolation', 'remove_rigid_rot', 'ion_temperature', 'tempw', 'tolp', 'delta_t', 'nraise', 'refold_pos', 'upscale', 'bfgs_ndim', 'trust_radius_max', 'trust_radius_min', 'trust_radius_ini', 'w_1', 'w_2', 'fire_alpha_init', 'fire_falpha', 'fire_nmin', 'fire_f_inc', 'fire_f_dec', 'fire_dtmax'],
    #
    '&CELL' : ['cell_dynamics', 'press', 'wmass', 'cell_factor', 'press_conv_thr' 'cell_dofree'],
    #
    '&FCP' : ['fcp_mu', 'fcp_dynamics', 'fcp_conv_thr', 'fcp_ndiis', 'fcp_mass','fcp_velocity', 'fcp_temperature', 'fcp_tempw', 'fcp_tolp ', 'fcp_delta_t', 'fcp_nraise', 'freeze_all_atoms'],
    #
    '&RISM' : ['nsolv', 'closure', 'tempv', 'ecutsolv', 'solute_lj', 'solute_epsilon', 'solute_sigma', 'starting1d', 'starting3d', 'smear1d', 'smear3d', 'rism1d_maxstep', 'rism3d_maxstep', 'rism1d_conv_thr', 'rism3d_conv_thr', 'mdiis1d_size', 'mdiis3d_size', 'mdiis1d_step', 'mdiis3d_step', 'rism1d_bond_width', 'rism1d_dielectric', 'rism1d_molesize', 'rism1d_nproc', 'rism3d_conv_level', 'rism3d_planar_average', 'laue_nfit', 'laue_expand_right', 'laue_expand_left', 'laue_starting_right', 'laue_starting_left', 'laue_buffer_right', 'laue_buffer_left', 'laue_both_hands', 'laue_wall', 'laue_wall_z', 'laue_wall_rho', 'laue_wall_epsilon', 'laue_wall_sigma', 'laue_wall_lj6'],
}
"""Dictionary with all possible NAMELISTs as keys, and the corresponding variables as values."""


pw_cards = {
    'ATOMIC_SPECIES' : ['X', 'Mass_X', 'PseudoPot_X'],
    #
    'ATOMIC_POSITIONS' : ['X', 'x', 'y', 'z', 'if_pos(1)', 'if_pos(2)', 'if_pos(3)'],
    #
    'K_POINTS' : ['nks', 'xk_x', 'xk_y', 'xk_z', 'wk', 'nk1', 'nk2', 'nk3', 'sk1', 'sk2', 'sk3'],
    #
    'ADDITIONAL_K_POINTS' : ['nks_add', 'k_x', 'k_y', 'k_z', 'wk_'],
    #
    'CELL_PARAMETERS': ['v1', 'v2', 'v3'],
    #
    'CONSTRAINTS' : ['nconstr', 'constr_tol', 'constr_type', 'constr(1)', 'constr(2)', 'constr(3)', 'constr(4)', 'constr_target'],
    #
    'OCCUPATIONS': ['f_inp1', 'f_inp2'],
    #
    'ATOMIC_VELOCITIES' : ['V', 'vx', 'vy', 'vz'],
    #
    'ATOMIC_FORCES' : ['X', 'fx', 'fy', 'fz'],
    #
    'SOLVENTS' : ['X', 'Density', 'Molecule', 'X', 'Density_Left', 'Density_Right', 'Molecule'],
    #
    'HUBBARD' : ['label(1)-manifold(1)', 'u_val(1)', 'label(1)-manifold(1)', 'j0_val(1)', 'paramType(1)', 'label(1)-manifold(1)', 'paramValue(1)', 'label(I)-manifold(I)', 'u_val(I)', 'label(I)-manifold(I)', 'j0_val(I)', 'label(I)-manifold(I)', 'label(J)-manifold(J)', 'I', 'J', 'v_val(I,J)'],
    # Extra card for output CELL_PARAMETERS
    'CELL_PARAMETERS_out': ['v1', 'v2', 'v3'],
    # Extra card for output ATOMIC_POSITIONS
    'ATOMIC_POSITIONS_out' : ['X', 'x', 'y', 'z', 'if_pos(1)', 'if_pos(2)', 'if_pos(3)'],
}
"""Dictionary with every possible CARDs as keys, and the corresponding variables as values."""


_pw_int_values = ['max_seconds', 'nstep', 'ibrav', 'nat', 'ntyp', 'dftd3_version', 'electron_maxstep']
"""Values from any namelist that must be integers"""


_upper_cards = pw_cards.keys()
_all_cards = []
for _upper_card in _upper_cards:
    _all_cards.append(_upper_card.lower())
_all_cards.extend(_upper_cards)
_all_cards_regex = '|'.join(_all_cards)
"""Regex string that matches all CARDS present in the file."""
_all_cards_regex = rf'(?!\s*!\s*)({_all_cards_regex})(?!\s*=)'

