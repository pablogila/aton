from aton.txt import find


sample = 'tests/samples/sample.txt'


def test_lines():
    assert find.lines(filepath=sample, key='5', matches=0, additional=0, split=False, regex=False) == ['line5']
    assert find.lines(filepath=sample, key='5', matches=-1, additional=0, split=False, regex=False) == ['line5']
    assert find.lines(filepath=sample, key='5', matches=1, additional=1, split=True, regex=False) == ['line5', 'line6']
    assert find.lines(filepath=sample, key='5', matches=1, additional=-1, split=True, regex=False) == ['line4', 'line5']
    assert find.lines(filepath=sample, key='5', matches=0, additional=0, split=False, regex=True) == ['line5']
    assert find.lines(filepath=sample, key='line', matches=1, additional=0, split=False, regex=True) == ['line1']
    assert find.lines(filepath=sample, key='line', matches=-1, additional=0, split=False, regex=True) == ['line9']
    assert find.lines(filepath=sample, key='line', matches=-2, additional=1, split=True, regex=False) == ['line8', 'line9', 'line9']
    assert find.lines(filepath=sample, key='line', matches=-2, additional=1, split=True, regex=True) == ['line8', 'line9', 'line9']


def test_lines_none():
    assert find.lines(filepath=sample, key='nonexisting', matches=0, additional=0, split=False, regex=False) == []
    assert find.lines(filepath=sample, key='nonexisting', matches=0, additional=0, split=False, regex=True) == []


def test_between():
    # With and without keys
    assert find.between(filepath=sample, key1='5', key2='7', include_keys=False, match=1, regex=False) == 'line6'
    assert find.between(filepath=sample, key1='5', key2='7', include_keys=True, match=1, regex=False) == 'line5\nline6\nline7'
    assert find.between(filepath=sample, key1='5', key2='7', include_keys=False, match=1, regex=True) == 'line6'
    assert find.between(filepath=sample, key1='5', key2='7', include_keys=True, match=1, regex=True) == 'line5\nline6\nline7'
    # Nonexisting second key, it should go all the way to the end
    assert find.between(filepath=sample, key1='5', key2='nonexisting', include_keys=True, match=1, regex=False) == 'line5\nline6\nline7\nline8\nline9'
    assert find.between(filepath=sample, key1='5', key2='nonexisting', include_keys=True, match=1, regex=True) == 'line5\nline6\nline7\nline8\nline9'
    # From the end
    assert find.between(filepath=sample, key1='5', key2='nonexisting', include_keys=True, match=-1, regex=False) == 'line5\nline6\nline7\nline8\nline9'
    assert find.between(filepath=sample, key1='5', key2='nonexisting', include_keys=True, match=-1, regex=True) == 'line5\nline6\nline7\nline8\nline9'
    # With repeated keys, it should go all the way to the end
    assert find.between(filepath=sample, key1='line5', key2='line5', include_keys=True, match=1, regex=False) == 'line5\nline6\nline7\nline8\nline9'
    assert find.between(filepath=sample, key1='line5', key2='line5', include_keys=True, match=1, regex=True) == 'line5\nline6\nline7\nline8\nline9'
    assert find.between(filepath=sample, key1='line5', key2='line5', include_keys=True, match=-1, regex=False) == 'line5\nline6\nline7\nline8\nline9'
    assert find.between(filepath=sample, key1='line5', key2='line5', include_keys=True, match=-1, regex=True) == 'line5\nline6\nline7\nline8\nline9'
    # Without including keys
    assert find.between(filepath=sample, key1='5', key2='nonexisting', include_keys=False, match=-1, regex=False) == 'line6\nline7\nline8\nline9'
    assert find.between(filepath=sample, key1='5', key2='nonexisting', include_keys=False, match=-1, regex=True) == 'line6\nline7\nline8\nline9'


def test_between_none():
    assert find.between(filepath=sample, key1='nonexisting', key2='7', include_keys=False, match=1, regex=False) == ''
    assert find.between(filepath=sample, key1='nonexisting', key2='nonexisting', include_keys=False, match=1, regex=False) == ''
    assert find.between(filepath=sample, key1='nonexisting', key2='7', include_keys=False, match=1, regex=True) == ''
    assert find.between(filepath=sample, key1='nonexisting', key2='nonexisting', include_keys=False, match=1, regex=True) == ''

