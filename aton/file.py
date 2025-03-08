"""
# Description

Functions to move files around.


# Index

| | |
| --- | --- |
| `save()`              | Save a Python object to a compressed binary file, as `.aton` |
| `load()`              | Load a Python object from a compressed binary file, as `.aton` |
| `get()`               | Check that a file exists, and return the full path |
| `get_list()`          | Get a list of the files inside a folder, applying optional filters |
| `get_dir()`           | Get the full path of a folder or the cwd |
| `copy()`              | Copy file |
| `move()`              | Move file |
| `remove()`            | Remove file or folder |
| `rename_on_folder()`  | Batch rename files from a folder |
| `rename_on_folders()` | Barch rename files from subfolders |
| `copy_to_folders()`   | Copy files to individual subfolders |

---
"""


import os
import shutil
import pickle
import gzip


def save(object, filename:str=None):
    """Save a Python object in the current working directory as a compressed binary `*.aton` file."""
    filename = 'data' if filename is None else filename
    if not filename.endswith('.aton'):
        filename += '.aton'
    file = os.path.join(os.getcwd(), filename)
    with gzip.open(file, 'wb') as f:
        pickle.dump(object, f)
    print(f"Data saved and compressed to {file}")


def load(filepath:str='data.aton'):
    """Load a Python object from a compressed binary `*.aton` file.

    Use only if you trust the person who sent you the file!
    """
    file_path = get(filepath, return_anyway=True)
    if not file_path:
        file_path = get(filepath + '.aton', return_anyway=True)
    if not file_path:
        raise FileNotFoundError(f"Missing file {filepath}")
    with gzip.open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data


def get(
        filepath,
        include=None,
        return_anyway:bool=False
        ) -> str:
    """Check if `filepath` exists, and returns its full path.

    Raises an error if the file is not found,
    unless `return_anyway = True`, in which case it returns None.
    This can be used to personalize errors.

    If the provided string is a directory, it checks the files inside it.
    if there is only one file inside, it returns said file;
    if there are more files, it tries to filter them with the `include` filters
    (string or list of strings) to return a single file.
    If this fails, try using more strict filters to return a single file.
    """
    if os.path.isfile(filepath):
        return os.path.abspath(filepath)
    elif os.path.isdir(filepath):
        files = get_list(folder=filepath, include=include, abspath=True)
    elif return_anyway:
        return None
    else:
        raise FileNotFoundError('Nothing found at ' + str(filepath))
    # Return a single file
    if len(files) == 1:
        return files[0]
    elif return_anyway:
        return None
    elif len(files) == 0:
        raise FileNotFoundError("The following directory is empty (maybe due to the 'include' filters):\n" + filepath)
    else:
        raise FileExistsError(f'More than one file found, please apply a more strict filter. Found:\n{files}')    


def get_list(
        folder:str=None,
        include=None,
        exclude=None,
        abspath:bool=True,
        also_folders:bool=False,
    ) -> list:
    """Return the files inside a `folder`, applying optional filters.

    Only filenames containing all strings in the `include` list will be returned.
    Filenames containing any string from the `exclude` list will be ignored.

    The full paths are returned by default; to get only the base names, set `abspath = False`.
    The CWD folder is used by default if no `folder` is provided.
    It also returns folders if `also_folders = True`.
    """
    if not folder:
        folder = os.getcwd()
    if os.path.isfile(folder):
        folder = os.path.dirname(folder)
    if not os.path.isdir(folder):
        raise FileNotFoundError('Directory not found: ' + folder)
    folder = os.path.abspath(folder)
    files = os.listdir(folder)
    if not files:
        return []
    # Absolute paths?
    if abspath:
        files = [os.path.join(folder, f) for f in files]
    # Should we keep only files?
    if not also_folders:
        files = [f for f in files if not os.path.isdir(f if abspath else os.path.join(folder, f))]
    # Apply filters if provided
    if include is not None:
        # Ensure include filters is always a list
        if not isinstance(include, list):
            include = [str(include)]
        # Normalize filter names
        include = [os.path.basename(i) for i in include]
        # Only keep files that contain all filters
        files = [f for f in files if all(filter_str in os.path.basename(f) for filter_str in include)]
    # Remove files containing any string from the exclude list
    if exclude is not None:
        # Ensure exclude filters is always a list
        if not isinstance(exclude, list):
            exclude = [str(exclude)]
        # Normalize ignoring filter names
        exclude = [os.path.basename(i) for i in exclude]
        # Exclude the corresponding files
        files = [f for f in files if not any(filter_str in os.path.basename(f) for filter_str in exclude)]
    return files


def get_dir(folder=None) -> str:
    """Returns the full path of `folder` or the parent folder if it's a file. If none is provided, the current working directory is returned."""
    if folder == None:
        path = os.getcwd()
    elif os.path.isdir(folder):
        path = os.path.realpath(folder)
    elif not os.path.isdir(folder):
        if os.path.isfile:
            path = os.path.dirname(folder)
            path = os.path.realpath(path)
        else:
            raise FileNotFoundError(f'Missing folder at {folder}')
    return path


def copy(
        old:str,
        new:str
    ) -> None:
    """Copies `old` file to `new` file"""
    # Yes, I know, why use ATON for this right? copy() and move() functions are here just for consistancy.
    file = shutil.copy(old, new)
    return None


def move(
        old:str,
        new:str
    ) -> None:
    """Moves `old` file to `new` file."""
    file = shutil.move(old, new)
    return None


def remove(filepath:str) -> None:
    """Removes the given file or folder at `filepath`.

    > WARNING: Removing stuff is always dangerous, be careful!
    """
    if filepath is None:
        return None  # It did not exist in the first place
    elif os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        return None  # It did not exist in the first place
    return None


def rename_on_folder(
        old:str,
        new:str,
        folder=None,
    ) -> None:
    """Batch renames files in the given `folder`.

    Replaces the `old` string by `new` string.
    If no folder is provided, the current working directory is used.
    """
    if folder is None:
        files = os.listdir('.')
    elif os.path.isdir(folder):
        file_list = os.listdir(folder)
        files = []
        for file in file_list:
            file_path = os.path.join(folder, file)
            files.append(file_path)
    elif os.path.isdir(os.path.join(os.getcwd(), folder)):
        folder_path = os.path.join(os.getcwd(), folder)
        file_list = os.listdir(folder_path)
        files = []
        for file in file_list:
            file_path = os.path.join(folder_path, file)
            files.append(file_path)
    else:
        raise FileNotFoundError('Missing folder at ' + folder + ' or in the CWD ' + os.getcwd())
    for f in files:
        if old in f:
            os.rename(f, f.replace(old, new))
    return None


def rename_on_folders(
        old:str,
        new:str,
        folder=None,
    ) -> None:
    """Renames the files inside the subfolders in the parent `folder`.
    
    Renames from an `old` string to the `new` string.
    If no `folder` is provided, the current working directory is used.
    """
    if folder is None:
        things = os.listdir('.')
    elif os.path.isdir(folder):
        things = os.listdir(folder)
    elif os.path.isdir(os.path.join(os.getcwd(), folder)):
        things = os.listdir(os.path.join(os.getcwd(), folder))
    else:
        raise FileNotFoundError('Missing folder at ' + folder + ' or in the CWD ' + os.getcwd())
    for d in things:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if old in f:
                    old_file = os.path.join(d, f)
                    new_file = os.path.join(d, f.replace(old, new))
                    os.rename(old_file, new_file)
    return None


def copy_to_folders(
        folder=None,
        extension:str=None,
        strings_to_delete:list=[],
    ) -> None:
    """Copies the files from the parent `folder` with the given `extension` to individual subfolders.

    The subfolders are named as the original files,
    removing the strings from the `strings_to_delete` list.
    If no `folder` is provided, it runs in the current working directory.
    """
    if folder is None:
        folder = os.getcwd()
    old_files = get_list(folder=folder, include=extension)
    if old_files is None:
        raise ValueError('No ' + extension + ' files found in path!')
    for old_file in old_files:
        new_file = old_file
        for string in strings_to_delete:
            new_file = new_file.replace(string, '')
        path = new_file.replace(extension, '')
        os.makedirs(path, exist_ok=True)
        new_file_path = os.path.join(path, new_file)
        copy(old_file, new_file_path)
    return None

