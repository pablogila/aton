from aton.st import file


folder = 'tests/samples/'
sample = folder + 'sample.txt'
sample_copy = folder + 'sample_copy.txt'
sample_copy_2 = folder + 'sample_copy_2.txt'
sample_ok = folder + 'sample_ok.txt'
sample_ok_2 = folder + 'sample_ok_2.txt'


def test_get():
    # Clean from previous tests
    try:
        file.remove(sample_copy)
    except:
        pass
    # Finds an existing file
    try:
        assert file.get(sample) != None
        assert True
    except FileNotFoundError:
        assert False
    # Does not find a non-existing file
    try:
        file.get(sample_copy)
        assert False
    except FileNotFoundError:
        assert True
    # get_list, 'tests/sample.txt' in 'fullpath/tests/sample.txt'
    try:
        assert sample in file.get_list(folder, filters='sample')[0]
    except:
        assert False


def test_copy():
    try:
        file.remove(sample_copy)
        file.remove(sample_copy_2)
    except:
        pass
    # Copy files
    try:
        file.copy(sample, sample_copy)
        assert file.get(sample_copy) != None
    except FileNotFoundError:
        assert False
    # Move files
    try:
        file.move(sample_copy, sample_copy_2)
        assert file.get(sample_copy_2) != None
    except:
        assert False
    try:
        file.get(sample_copy)
        assert False
    except FileNotFoundError:
        assert True
    # Remove
    try:
        file.remove(sample_copy_2)
    except:
        assert False
    try:
        file.get(sample_copy_2)
        assert False
    except:
        assert True


def test_rename():
    try:
        file.remove(sample_copy)
        file.remove(sample_ok)
    except:
        pass
    file.copy(sample, sample_copy)
    file.rename_on_folder(old='copy', new='ok', folder=folder)
    try:
        file.remove(sample_ok)
        assert True
    except:
        assert False
    try:
        file.remove(sample_copy)
        assert False
    except:
        assert True


def test_folders():
    try:
        file.remove(sample_copy)
        file.remove(sample_copy_2)
        file.remove(sample_ok)
        file.remove(sample_ok_2)
    except:
        pass
    file.copy_to_folders(extension='.txt', strings_to_delete=['.txt'], folder=folder)
    try:
        assert file.get_list(folder=folder+'sample', abspath=False) == ['sample.txt']
    except:
        assert False
    # Check that the folder is deleted
    file.remove(folder+'sample')
    try:
        x = file.get_list(folder+'sample')
        print(x)
        assert False
    except FileNotFoundError:
        assert True

