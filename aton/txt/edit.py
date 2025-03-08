"""
# Description

Functions to manipulate the content of text files.


# Index

`insert_at()`  
`insert_under()`  
`replace()`  
`replace_line()`  
`replace_between()`  
`delete_under()`  
`correct_with_dict()`  
`from_template()`  

---
"""


import mmap
from . import find
import aton.file as file


def insert_at(
        filepath,
        text:str,
        position:int
    ) -> None:
    """Inserts a `text` in the line with `position` index of a given `filepath`.

    If `position` is negative, starts from the end of the file.
    """
    file_path = file.get(filepath)
    with open(file_path, 'r+') as f:
        lines = f.read().splitlines()
        if position < 0:
            position = len(lines) + position + 1
        if position < 0 or position > len(lines):
            raise IndexError("Position out of range")
        lines.insert(position, text)
        f.seek(0)
        f.write('\n'.join(lines))
        f.truncate()
    return None


def insert_under(
        filepath,
        key:str,
        text:str,
        insertions:int=0,
        skips:int=0,
        regex:bool=False
    ) -> None:
    """Inserts a `text` under the line(s) containing the `key` in `filepath`.

    The keyword can be at any position within the line.
    Regular expressions can be used by setting `regex=True`. 

    By default all matches are inserted with `insertions=0`,
    but it can insert only a specific number of matches
    with positive numbers (1, 2...), or starting from the bottom with negative numbers.

    The text can be introduced after a specific number of lines after the match,
    changing the value `skips`. Negative integers introduce the text in the previous lines.
    """
    file_path = file.get(filepath)
    if regex:
        positions = find.pos_regex(file_path, key, insertions)
    else:
        positions = find.pos(file_path, key, insertions)
    positions.reverse()  # Must start replacing from the end, otherwise the atual positions may change!
    # Open the file in read-write mode
    with open(file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as mm:
            # Get the places to insert the text
            for position in positions:
                start, end = find.line_pos(mm, position, skips)
                inserted_text = '\n' + text # Ensure we end in a different line
                if end == 0: # If on the first line
                    inserted_text = text + '\n'
                remaining_lines = mm[end:]
                new_line = inserted_text.encode()
                updated_content = new_line + remaining_lines
                mm.resize(len(mm) + len(new_line))
                mm[end:] = updated_content
    return None


def replace(
        filepath:str,
        key:str,
        text:str,
        replacements:int=0,
        regex:bool=False
    ) -> None:
    """Replaces the `key` with `text` in `filepath`.

    It can also be used to delete the keyword with `text=''`.
    To search with regular expressions, set `regex=True`.

    The value `replacements` specifies the number of replacements to perform:
    1 to replace only the first keyword found, 2, 3...
    Use negative values to replace from the end of the file,
    eg. to replace the last found key, use `replacements=-1`.
    To replace all values, set `replacements = 0`, which is the value by default.

    ```
    line... key ...line -> line... text ...line
    ```
    """
    file_path = file.get(filepath)
    if regex:
        positions = find.pos_regex(file_path, key, replacements)
    else:
        positions = find.pos(file_path, key, replacements)
    positions.reverse()  # Must start replacing from the end, otherwise the atual positions may change!
    with open(file_path, 'r+') as f:
        content = f.read()
        for start, end in positions:
            content = "".join([content[:start], text, content[end:]])
        f.seek(0)
        f.write(content)
        f.truncate()
    return None


def replace_line(
        filepath:str,
        key:str,
        text:str,
        replacements:int=0,
        skips:int=0,
        additional:int=0,
        regex:bool=False,
        raise_errors:bool=False,
    ) -> None:
    """Replaces the entire line(s) containing the `key` with the `text` in `filepath`.

    It can be used to delete line(s) by setting `text=''`.
    Regular expressions can be used with `regex=True`.

    The value `replacements` specifies the number of lines to replace:
    1 to replace only the first line with the keyword, 2, 3...
    Use negative values to replace from the end of the file,
    e.g., to replace only the last line containing the keyword, use `replacements = -1`.
    To replace all lines, set `replacements = 0`, which is the value by default.

    The default line to replace is the matching line,
    but it can be any other specific line after or before the matching line;
    this is indicated with `skips` as a positive or negative integer.

    More lines can be replaced with `additional` lines (int).
    Note that the matched line plus the additional lines
    will be replaced, this is, additional lines +1.
    """
    file_path = file.get(filepath)
    if regex:
        positions = find.pos_regex(file_path, key, replacements)
    else:
        positions = find.pos(file_path, key, replacements)
    positions.reverse()  # Must start replacing from the end, otherwise the atual positions may change!
    if positions == [] and raise_errors:
        raise ValueError(f'The line could not be replaced because the following key was not found:\n{key}')
    # Open the file in read-write mode
    with open(file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as mm:
            for position in positions:
                # Get the positions of the full line containing the match
                line_start, line_end = find.line_pos(mm, position, skips)
                # Additional lines
                if additional > 0:
                    for _ in range(abs(additional)):
                        line_end = mm.find(b'\n', line_end + 1, len(mm)-1)
                        if line_end == -1:
                            line_end = len(mm) - 1
                            break
                elif additional < 0:
                    for _ in range(abs(additional)):
                        line_start = mm.rfind(b'\n', 0, line_start - 1) + 1
                        if line_start == -1:
                            line_start = 0
                            break
                # Replace the line
                old_line = mm[line_start:line_end]
                new_line = text.encode()
                if text == '':  # Delete the line, and the extra \n
                    remaining_content = mm[line_end:]
                    mm.resize(len(mm) - len(old_line) - 1)
                    mm[line_start-1:] = remaining_content
                # Directly modify the memory-mapped region
                elif len(new_line) == len(old_line):
                    mm[line_start:line_end] = new_line
                else:  # Adjust content for differing line sizes
                    remaining_content = mm[line_end:]
                    updated_content = new_line + remaining_content
                    mm.resize(len(mm) + len(new_line) - len(old_line))
                    mm[line_start:] = updated_content
    return None


def replace_between(
        filepath:str,
        key1:str,
        key2:str,
        text:str,
        delete_keys:bool=False,
        from_end:bool=False,
        regex:bool=False
    ) -> None:
    """Replace with `text` between keywords `key1` and `key2` in `filepath`.

    It can be used to delete the text between the keys by setting `text=''`.
    Regular expressions can be used by setting `regex=True`.

    Key lines are also deleted if `delete_keys=True`.

    Only the first matches of the keywords are used by default;
    you can use the last ones with `from_end = True`.
    ```
    lines...
    key1
    text
    key2
    lines...
    ```
    """
    file_path = file.get(filepath)
    index = 1
    if from_end:
        index = -1
    start, end = find.between_pos(file_path, key1, key2, delete_keys, index, regex)
    with open(file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as mm:
            # Replace the line
            old_content = mm[start:end]
            new_content = text.encode()
            if text == '':  # Delete the line, and the extra \n
                remaining_content = mm[end:]
                mm.resize(len(mm) - len(old_content) - 1)
                mm[start-1:] = remaining_content
            # Directly modify the memory-mapped region
            elif len(new_content) == len(old_content):
                mm[start:end] = new_content
            else:  # Adjust the content for differing line sizes
                remaining_content = mm[end:]
                updated_content = new_content + remaining_content
                mm.resize(len(mm) + len(new_content) - len(old_content))
                mm[start:] = updated_content
    return None


def delete_under(
        filepath,
        key:str,
        match:int=1,
        skips:int=0,
        regex:bool=False
    ) -> None:
    """Deletes all the content under the line containing the `key` in `filepath`.

    The keyword can be at any position within the line.
    Regular expressions can be used by setting `regex=True`.

    By default the first `match` is used; it can be any positive integer (0 is treated as 1!),
    including negative integers to select a match starting from the end of the file.

    The content can be deleted after a specific number of lines after the match,
    changing the value `skips`, that skips the specified number of lines.
    Negative integers start deleting the content from the previous lines.
    """
    file_path = file.get(filepath)
    if match == 0:
        match = 1
    if regex:
        positions = find.pos_regex(file_path, key, match)
    else:
        positions = find.pos(file_path, key, match)
    if match > 0:  # We only want one match, and should be the last if matches > 0
        positions.reverse()
    position = positions[0]
    # Open the file in read-write mode
    with open(file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as mm:
            # Get the places to insert the text
            start, end = find.line_pos(mm, position, skips)
            mm.resize(len(mm) - len(mm[end:]))
            mm[end:] = b''
    return None


def correct_with_dict(
        filepath:str,
        correct:dict
    ) -> None:
    """Corrects the given text file `filepath` using a `correct` dictionary."""
    file_path = file.get(filepath)
    with open(file_path, 'r+') as f:
        content = f.read()
        for key, value in correct.items():
            content = content.replace(key, value)
        f.seek(0)
        f.write(content)
        f.truncate()
    return None


def from_template(
        old:str,
        new:str,
        correct:dict=None,
        comment:str=None,
    ) -> None:
    """Creates `new` file from `old`, replacing values from a `correct` dict, inserting a `comment` on top."""
    file.copy(old, new)
    if comment:
        insert_at(new, comment, 0)
    if correct:
        correct_with_dict(new, correct)
    return None

