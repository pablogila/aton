from aton.txt import extract


def test_extract_number():
    assert extract.number(' test = 123 number ', 'test') == 123.0
    assert extract.number(' test 123 number ', 'test') == 123.0


def test_extract_string():
    assert extract.string(text=' test = "hello" stop ', name='test', stop='stop', strip=True) == 'hello'
    assert extract.string(text=' test "hello" stop ', name='test', stop='stop', strip=True) == 'hello'
    assert extract.string(text=" test 'hello' stop ", name='test', stop='stop', strip=True) == 'hello'
    assert extract.string(text=" test 'hello' stop ", name='test', stop='stop', strip=False) == "'hello'"


def test_extract_column():
    assert extract.column(' 123 456.5 789  ', 2) == '789'


def test_extract_coords():
    assert extract.coords('coordinates: 1.0, 2.0 and 3 these were the coordinates') ==[1.0, 2.0, 3.0]


def test_extract_element():
    string = '  element I Lead Pb Nitrogen H2, Xx2 fake element, O Oxygen, He4 isotope Ag Element '
    assert extract.element(text=string, index=0) == 'I'
    assert extract.element(text=string, index=1) == 'Pb'
    assert extract.element(text=string, index=2) == 'H2'
    assert extract.element(text=string, index=3) == 'O'
    assert extract.element(text=string, index=4) == 'He4'
    assert extract.element(text=string, index=5) == 'Ag'


def test_extract_isotope():
    assert extract.isotope('He4') == ('He', 4)
    assert extract.isotope('He5') == ('He', 5)
    assert extract.isotope('Au') == ('Au', 0)
    try:
        extract.isotope('X')
        assert False, "Expected KeyError for non-existent element!"
    except KeyError:
        assert True
    try:
        extract.isotope('H9')
        assert False, "Expected KeyError for unrecognized isotope!"
    except KeyError:
        assert True

