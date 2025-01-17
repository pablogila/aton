import aton


folder = 'tests/samples/'


def test_normalize_cell_params():
    cell_params = 'CELL_PARAMETERS (alat= 10.0000)\n    1.00000000000   0.000000000   0.000000000\n   0.000000000   1.000000000   0.000000000 \n 0.000000000   0.000000000   1.0000000 '
    ideal_params = [
        'CELL_PARAMETERS alat= 10.0',
        '1.000000000000000   0.000000000000000   0.000000000000000',
        '0.000000000000000   1.000000000000000   0.000000000000000',
        '0.000000000000000   0.000000000000000   1.000000000000000',]
    normalized_params = aton.interface.qe.normalize_card(cell_params)
    assert normalized_params == ideal_params
    # Now check as a list
    cell_params = cell_params.splitlines()
    # With bohr values
    cell_params[0] = r' CELL_PARAMETERS {bohr}'
    ideal_params[0] = 'CELL_PARAMETERS bohr'
    normalized_params = aton.interface.qe.normalize_card(cell_params)
    assert normalized_params == ideal_params
    # With armstrong values
    cell_params[0] = r' CELL_PARAMETERS {angstrom}'
    ideal_params[0] = 'CELL_PARAMETERS angstrom'
    normalized_params = aton.interface.qe.normalize_card(cell_params)
    assert normalized_params == ideal_params


def test_normalize_atomic_positions():
    atomic_positions = " ATOMIC_POSITIONS {crystal} \n I   5.000000   0.0000000000000   0.000000000000000 \n C   0.000000000000000   5.000000000000000000   0.000000 "
    ideal_positions = [
        'ATOMIC_POSITIONS crystal',
        'I   5.000000000000000   0.000000000000000   0.000000000000000',
        'C   0.000000000000000   5.000000000000000   0.000000000000000']
    normalized_positions = aton.interface.qe.normalize_card(atomic_positions)
    assert normalized_positions == ideal_positions


def test_normalize_atomic_species():
    atomic_species = " ATOMIC_SPECIES \n     I  126.90400   I.upf  \nHe4   4.0026032497   He.upf\n\n! C   12.01060   C.upf\n ATOMIC_POSITIONS\n '  I   5.000000000000000   0.000000000000000   0.000000000000000'"
    ideal_species = ['ATOMIC_SPECIES', 'I   126.904   I.upf', 'He4   4.0026032497   He.upf']
    normalized_species = aton.interface.qe.normalize_card(atomic_species)
    assert normalized_species == ideal_species


def test_read():
    ideal = {
        # relax.out
        'Energy'               : -1000.0,
        'Volume'               : 2.0,
        'Density'              : 1.0,
        'Alat'                 : 10,
        'BFGS converged'       : True,
        'BFGS failed'          : False,
        'Total force'          : 0.000001,
        'Total SCF correction' : 0.0,
        'ibrav'                : 1,
        'Runtime'              : '48m 8.71s',
        'CELL_PARAMETERS_out'  : [
            'CELL_PARAMETERS alat= 10.0',
            '1.000000000   0.000000000   0.000000000',
            '0.000000000   1.000000000   0.000000000',
            '0.000000000   0.000000000   1.000000000'],
        'ATOMIC_POSITIONS_out' : [
            'ATOMIC_POSITIONS crystal',
            'I                1.0000000000        0.0000000000        0.0000000000',
            'C                0.0000000000        1.0000000000        0.0000000000',
            'N                0.0000000000        0.0000000000        1.0000000000'],
        # relax.in
        'K_POINTS'             : [
            'K_POINTS automatic',
            '2 2 2 0 0 0'],
        'ecutwfc'              : 60.0,
        'etot_conv_thr'        : 1.0e-12,
        'max_seconds'          : 1000,
        'pseudo_dir'           : "'./pseudos/'",
        'CELL_PARAMETERS' : [
            'CELL_PARAMETERS alat',
            '2.000000000000000   0.000000000000000   0.000000000000000',
            '0.000000000000000   2.000000000000000   0.000000000000000',
            '0.000000000000000   0.000000000000000   2.000000000000000'],
        'ATOMIC_SPECIES'       : [
            'ATOMIC_SPECIES',
            'I  126.90400   I.upf',
            'N   14.00650   N.upf',
            'C   12.01060   C.upf'],
        'ATOMIC_POSITIONS'     : [
            'ATOMIC_POSITIONS crystal',
            'I   5.000000000000000   0.000000000000000   0.000000000000000',
            'C   0.000000000000000   5.000000000000000   0.000000000000000',
            'N   0.000000000000000   0.000000000000000   5.000000000000000'],
    }
    result = aton.interface.qe.read_dir(folder=folder, in_str='relax.in', out_str='relax.out')
    for key in ideal:
        if key in aton.interface.qe.pw_cards:
            ideal[key] = aton.interface.qe.normalize_card(ideal[key])
        assert result[key] == ideal[key]


def test_scf_from_relax():
    ideal = {
        'calculation'      : "'scf'",
        'celldm(1)'        : 10.0,
        'ibrav'            : 0,
        'occupations'      : "'fixed'",
        'conv_thr'         : 2.0e-12,
        'ATOMIC_SPECIES'   : [
            'ATOMIC_SPECIES',
            'I  126.90400   I.upf',
            'N   14.00650   N.upf',
            'C   12.01060   C.upf'],
        'CELL_PARAMETERS'  : [
            'CELL_PARAMETERS alat',
            '1.000000000   0.000000000   0.000000000',
            '0.000000000   1.000000000   0.000000000',
            '0.000000000   0.000000000   1.000000000'],
        'ATOMIC_POSITIONS' : [
            'ATOMIC_POSITIONS crystal',
            'I                1.0000000000        0.0000000000        0.0000000000',
            'C                0.0000000000        1.0000000000        0.0000000000',
            'N                0.0000000000        0.0000000000        1.0000000000'],
    }
    aton.interface.qe.scf_from_relax(folder=folder)
    result = aton.interface.qe.read_in(folder + 'scf.in')
    for key in ideal:
        if key in ['ATOMIC_SPECIES', 'CELL_PARAMETERS', 'CELL_PARAMETERS_out', 'ATOMIC_POSITIONS', 'ATOMIC_POSITIONS_out']:
            ideal[key] = aton.interface.qe.normalize_card(ideal[key])
        assert result[key] == ideal[key]
    assert 'A' not in result.keys()
    try:
        aton.st.file.remove(folder + 'scf.in')
    except:
        pass


def test_update_other_values():
    tempfile = folder + 'temp.in'
    aton.st.file.copy(folder + 'relax.in', tempfile)
    aton.interface.qe.set_value(tempfile, 'celldm(1)', 10.0)
    modified = aton.interface.qe.read_in(tempfile)
    assert 'A' not in modified.keys()
    aton.st.file.remove(tempfile)


def test_set_value():
    tempfile = folder + 'temp.in'
    aton.st.file.copy(folder + 'relax.in', tempfile)
    aton.interface.qe.set_value(tempfile, 'ecutwfc', 80.0)
    aton.interface.qe.set_value(tempfile, 'ibrav', 5)
    aton.interface.qe.set_value(tempfile, 'calculation', "'vc-relax'")
    aton.interface.qe.set_value(tempfile, 'celldm(1)', 10.0)
    modified = aton.interface.qe.read_in(tempfile)
    # Check some unmodified values
    assert modified['max_seconds'] == 1000
    assert modified['input_dft'] == "'PBEsol'"
    # Check the modified
    assert 'A' not in modified.keys()
    assert modified['ecutwfc'] == 80.0
    assert modified['ibrav'] == 5
    assert modified['calculation'] == "'vc-relax'"
    assert modified['celldm(1)'] == 10.0
    aton.interface.qe.set_value(tempfile, 'celldm(1)', '')
    modified = aton.interface.qe.read_in(tempfile)
    assert 'A' not in modified.keys()
    assert 'celldm(1)' not in modified.keys()
    aton.st.file.remove(tempfile)


def test_count_elements():
    atomic_positions = [
        'ATOMIC_POSITIONS crystal',
        'I   5.0000000000        0.0000000000        0.0000000000',
        'C   0.0000000000        5.0000000000        0.0000000000',
        'N   0.0000000000        0.0000000000        5.0000000000',
        'Cl   0.0  0.0  0.0',
        'Cl  1.0  1.0  1.0']
    ideal = {'I': 1, 'C': 1, 'N': 1, 'Cl': 2}
    obtained = aton.interface.qe.count_elements(atomic_positions)
    for key in ideal.keys():
        assert ideal[key] == obtained[key]
    # Again, in case it does something weird
    obtained = aton.interface.qe.count_elements(atomic_positions)
    for key in ideal.keys():
        assert ideal[key] == obtained[key]


def test_add_atom():
    ideal_positions = [
        'ATOMIC_POSITIONS crystal',
        'I                5.0000000000        0.0000000000        0.0000000000',
        'C                0.0000000000        5.0000000000        0.0000000000',
        'N                0.0000000000        0.0000000000        5.0000000000',
        'O   0.0  0.0  0.0',
        'Cl  1.0  1.0  1.0']
    ideal_positions = aton.interface.qe.normalize_card(ideal_positions)
    tempfile = folder + 'temp.in'
    aton.st.file.copy(folder + 'relax.in', tempfile)
    position_1 = '  O   0.0   0.0   0.0'
    position_2 = ['Cl', 1.0, 1.0, 1.0]
    aton.interface.qe.add_atom(filepath=tempfile, position=position_1)
    aton.interface.qe.add_atom(filepath=tempfile, position=position_2)
    temp = aton.interface.qe.read_in(tempfile)
    nat = temp['nat']
    ntyp = temp['ntyp']
    atomic_positions = temp['ATOMIC_POSITIONS']
    assert nat == 5
    assert ntyp == 5
    number_of_elements = aton.interface.qe.count_elements(atomic_positions)
    ideal_dict = {'I':1, 'C':1, 'N':1, 'O':1, 'Cl':1}
    for key in ideal_dict.keys():
        assert ideal_dict[key] == number_of_elements[key]
    # Assert we have the same ATOMIC_POSITIONS
    for i, ideal in enumerate(ideal_positions):
        ideal_str = ideal.split()
        detected_str = atomic_positions[i].split()
        assert detected_str == ideal_str
    # Additional surrounding values, just in case
    assert temp['ibrav'] == 1
    assert temp['A'] == 10.0
    assert temp['ecutwfc'] == 60.0
    assert temp['input_dft'] == "'PBEsol'"
    aton.st.file.remove(tempfile)


def test_get_atom():
    relax = folder + 'relax.in'
    ideal = 'N   0.000000000000000   0.000000000000000   5.000000000000000'
    approx_list_1 = [0.00, 0.00, 5.0001]
    approx_list_2 = [0.0, 0.0, 4.9999]
    approx_str = '0.0000, 0.0000, 5.0001'
    assert aton.interface.qe.get_atom(filepath=relax, position=approx_list_1, precision=3) == ideal
    assert aton.interface.qe.get_atom(filepath=relax, position=approx_list_2, precision=3) == ideal
    assert aton.interface.qe.get_atom(filepath=relax, position=approx_str, precision=3) == ideal

