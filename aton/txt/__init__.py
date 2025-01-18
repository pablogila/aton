"""
# General text operations

This subpackage contains tools for general text operations.
It provides the basic functionality that powers more complex subpackages,
such as `aton.interface`.


# Index

| | |
| --- | --- |
| `aton.txt.find`    | Search for specific content from a text file |
| `aton.txt.edit`    | Edit specific content from a text file |
| `aton.txt.extract` | Extract data from raw text strings |


# Examples

The following example shows how to find a value in a text file, extract it and paste it into another file using the txt subpackage:

```python
from aton import txt
# Get an array with all matches
alat_lines = txt.find.lines('relax.out', 'Lattice parameter =')
# Extract the numerical value of the last match
alat = txt.extract.number(alat_lines[-1], 'Lattice parameter')
# Paste it into another file
txt.edit.replace_line('scf.in', 'Lattice parameter =', f'Lattice parameter ='{alat})
```

Advanced usage such as regular expression matching or
additional line extraction is detailed in the API documentation.

"""


from . import find
from . import edit
from . import extract

