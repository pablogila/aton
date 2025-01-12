"""
# General text operations

This subpackage contains tools for general text operations.
It provides the basic functionality that powers more complex subpackages,
such as `aton.interface`.


# Index

| | |
| --- | --- |
| `aton.text.find`    | Search for specific content from a text file |
| `aton.text.edit`    | Edit specific content from a text file |
| `aton.text.extract` | Extract data from raw text strings |


# Examples

The following example shows how to find a value in a text file, extract it and paste it into another file using the text subpackage:

```python
from aton import text
# Get an array with all matches
alat_lines = text.find.lines('relax.out', 'Lattice parameter =')
# Extract the numerical value of the last match
alat = text.extract.number(alat_lines[-1], 'Lattice parameter')
# Paste it into another file
text.edit.replace_line('scf.in', 'Lattice parameter =', f'Lattice parameter ='{alat})
```

Advanced usage such as regular expression matching or
additional line extraction is detailed in the API documentation.

"""


from . import find
from . import edit
from . import extract

