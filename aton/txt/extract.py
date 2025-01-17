"""
# Description

Functions to extract data from raw text strings.


# Index

`number()`  
`string()`  
`column()`  
`coords()`  
`element()`  


# Examples

To extract a float value from a string,
```python
from aton import txt
line = 'energy =   500.0 Ry'
txt.extract.number(line, 'energy')
# 500.0  (float output)
```

To extract a text value, after and before specific strings,
```python
line = 'energy =   500.0 Ry were calculated'
txt.extract.string(line, 'energy', 'were')
# '500.0 Ry'  (String output)
```

To extract a float value from a specific column,
```python
# Name, Energy, Force, Error
line = 'Testing    1.1    1.2    0.3'
energy = txt.extract.column(line, 1)
# 1.1
```

To extract coordinates,
```python
line = ' He  0.10  0.20  0.30 '
txt.extract.coords(line)
# [0.1, 0.2, 0.3]  (List of floats)
```

To extract chemical elements,
```python
line = ' He4  0.10  Ag  0.20  Pb  0.30 '
first_element = txt.extract.element(line, 0)
# 'He4'
third_element = txt.extract.element(line, 2)
# 'Pb'
```

---
"""


import re
import aton.phys as phys


def number(
        text:str,
        name:str=''
    ) -> float:
    """Extracts the float value of a given `name` variable from a raw `text`."""
    if text == None:
        return None
    pattern = re.compile(rf"{name}\s*[:=]?\s*(-?\d+(?:\.\d+)?(?:[eEdD][+\-]?\d+)?)")
    match = pattern.search(text)
    if match:
        return float(match.group(1))
    return None
    

def string(
        text:str,
        name:str='',
        stop:str='',
        strip:bool=True
    ) -> str:
    """Extracts the `text` value of a given `name` variable from a raw string. Stops before an optional `stop` string.

    Removes leading and trailing commas by default, change this with `strip = False`.
    """
    pattern = re.compile(rf"{name}\s*[:=]?\s*(.*)")
    if stop:
        pattern = re.compile(rf"{name}\s*[:=]?\s*(.*)(?={stop})")
    match = re.search(pattern, text)
    if not match:
        return None
    result = str(match.group(1))
    result = result.strip()
    if strip:
        result = result.strip("'")
        result = result.strip('"')
        result = result.strip()
    return result


def column(
        text:str,
        column:int=0
    ) -> float:
    """Extracts the desired float `column` index of a given `string` (0 by default)."""
    if text is None:
        return None
    columns = text.split()
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    if column < len(columns):
        match = re.match(pattern, columns[column])
        if match:
            return float(match.group(1))
    return None


def coords(text:str) -> list:
    """Returns a list with the float coordinates expressed in a given `text` string."""
    if text is None:
        return None
    columns = re.split(r'[,\s]+', text.strip())
    pattern = r'(-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)'
    matches = []
    for column in columns:
        match = re.match(pattern, column)
        if match:
            matches.append(float(match.group(1)))
    return matches


def element(text:str, index:int=0) -> str:
    """Extract a chemical element from a raw `text` string.

    If there are several elements, you can return a specific `index` match (positive, 0 by default).
    Allows for standard elements (H, He, Na...) and isotopes (H2, He4...).
    """
    if text is None:
        return None
    columns = re.split(r'[,\s]+', text.strip())
    pattern = r'\s*([A-Z][a-z]{0,2}\d{0,3})(?=\s|$)'
    matches = []
    for column in columns:
        match = re.match(pattern, column)
        if match:
            matches.append(str(match.group(1)))
    # We have a list with possible matches. Let's determine which are actual elements.
    found_elements = []
    for possible_element in matches:
        possible_element = possible_element.strip()
        if not possible_element in phys.atoms.keys():
            try:
                element, isotope = phys.split_isotope(possible_element)
            except:  # It is not a valid atom
                continue
        found_elements.append(possible_element)
    if len(found_elements) <= index:
        return found_elements[-1]
    return found_elements[index]

