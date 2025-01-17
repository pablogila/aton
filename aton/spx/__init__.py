"""
# Spectra analysis

This module contains spectral analysis tools.


# Index

| | |
| --- | --- |
| `aton.spx.classes`   | Definition of the `Spectra`, `Plotting` and `Material` classes, instantiated as `aton.spx.Class()` |
| `aton.spx.fit`       | Spectral fitting functions |
| `aton.spx.normalize` | Spectra normalisation |
| `aton.spx.deuterium` | Deuteration estimation functions |
| `aton.spx.samples`   | Material definition examples |
| `aton.spx.plot`      | Spectra plotting, as `aton.spx.plot(Spectra)` |


# Examples

To load two INS spectra CSV files with cm$^{-1}$ as input units,
and plot them in meV units, normalizing their heights over the range from 20 to 50 meV:
```python
from aton import spx
# Set plotting parameters
plotting_options = spx.Plotting(
    title     = 'Calculated INS',
    )
# Load the spectral data
ins = spx.Spectra(
    type     = 'INS',
    files    = ['example_1.csv', 'example_2.csv'],
    units_in = 'cm-1',
    units    = 'meV',
    plotting = plotting_options,
    )
# Normalize the spectra
spx.height(spectra=ins, range=[20, 50])
# Plot the spectra
spx.plot(ins)
```

More examples in the [`Aton/examples/`](https://github.com/pablogila/Aton/tree/main/examples) folder.

"""

from .classes import Spectra, Plotting, Material
from . import fit
from . import normalize
from . import deuterium
from . import samples
from .plot import plot

