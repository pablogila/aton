from aton.txt import edit
from aton.st import file


folder = 'tests/samples/'
sample = folder + 'sample.txt'
sample_copy = folder + 'sample_copy.txt'


def test_insert_at():
    file.copy(sample, sample_copy)
    edit.insert_at(filepath=sample_copy, text='MIDDLE', position=1)
    edit.insert_at(filepath=sample_copy, text='START', position=0)
    edit.insert_at(filepath=sample_copy, text='END', position=-1)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'START\nline1\nMIDDLE\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nEND'
    edit.insert_at(filepath=sample_copy, text='AGAIN', position=6)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'START\nline1\nMIDDLE\nline2\nline3\nline4\nAGAIN\nline5\nline6\nline7\nline8\nline9\nEND'
    file.remove(sample_copy)


def test_insert_under():
    file.copy(sample, sample_copy)
    edit.insert_under(filepath=sample_copy, key='5', text='!!!', skips=0)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\nline5\n!!!\nline6\nline7\nline8\nline9'
    file.copy(sample, sample_copy)
    edit.insert_under(filepath=sample_copy, key='5', text='!!!', skips=-1)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\n!!!\nline5\nline6\nline7\nline8\nline9'
    file.copy(sample, sample_copy)
    edit.insert_under(filepath=sample_copy, key=r'l[a-z]*5', text='!!!', regex=True)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\nline5\n!!!\nline6\nline7\nline8\nline9'
    file.copy(sample, sample_copy)
    edit.insert_under(filepath=sample_copy, key=r'l[a-z]*4', text='!!!', insertions=1, regex=True)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\n!!!\nline5\nline6\nline7\nline8\nline9'
    file.remove(sample_copy)


def test_replace():
    file.copy(sample, sample_copy)
    edit.replace(filepath=sample_copy, key='line5', text='!!!')
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\n!!!\nline6\nline7\nline8\nline9'
    file.remove(sample_copy)


def test_replace_line():
    file.copy(sample, sample_copy)
    edit.replace_line(filepath=sample_copy, key='line5', text='!!!')
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\n!!!\nline6\nline7\nline8\nline9'
    file.copy(sample, sample_copy)
    edit.replace_line(filepath=sample_copy, key='line5', text='')
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\nline6\nline7\nline8\nline9'
    file.remove(sample_copy)


def test_replace_between():
    file.copy(sample, sample_copy)
    edit.replace_between(filepath=sample_copy, key1='line4', key2='line7', text='!!!')
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\n!!!\nline7\nline8\nline9'
    file.remove(sample_copy)


def test_remove_between():
    file.copy(sample, sample_copy)
    edit.replace_between(filepath=sample_copy, key1='line4', key2='line7', text='')
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\nline7\nline8\nline9'
    file.remove(sample_copy)


def test_delete_under():
    file.copy(sample, sample_copy)
    edit.delete_under(filepath=sample_copy, key='5')
    with open(sample_copy, 'r') as f:
        assert f.read() == 'line1\nline2\nline3\nline4\nline5'
    file.remove(sample_copy)


def test_correct_with_dict():
    correct = {'line1': 'text', 'line5': ''}
    file.copy(sample, sample_copy)
    edit.correct_with_dict(filepath=sample_copy, correct=correct)
    with open(sample_copy, 'r') as f:
        assert f.read() == 'text\nline2\nline3\nline4\n\nline6\nline7\nline8\nline9'
    file.remove(sample_copy)


def test_template():
    try:
        file.remove(sample_copy)
    except:
        pass
    try:
        edit.from_template(old=sample, new=sample_copy, correct={'line':''}, comment='!!!')
        with open(sample_copy, 'r') as f:
            content = f.read()
            assert content == '!!!\n1\n2\n3\n4\n5\n6\n7\n8\n9'
    except:
        assert False
    try:
        file.remove(sample_copy)
    except:
        pass

