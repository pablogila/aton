"""
# Description

This module contains spectral analysis tools.


# Index

| | |
| --- | --- |
| `aton.spectra.classes` | Class definitions of the `Spectra`, `Plotting`, `Scaling` and `Material` objects, instantiated as `aton.spectra.Class()` |
| `aton.spectra.fit` | Spectral fitting functions |
| `aton.spectra.normalize` | Spectra normalisation |
| `aton.spectra.deuterium` | Deuteration estimation functions |
| `aton.spectra.samples` | Material definition examples |
| `aton.spectra.plot` | Spectra plotting, as `spectra.plot(Spectra)` |


# Examples

To load two INS spectra CSV files with cm$^{-1}$ as input units,
and plot them in meV units, normalizing their heights over the range from 20 to 50 meV:
```python
from aton import spectra
ins = spectra.Spectra(
    type     = 'INS',
    files    = ['example_1.csv', 'example_2.csv'],
    units_in = 'cm-1',
    units    = 'meV',
    plotting = spectra.Plotting(
        title     = 'Calculated INS',
        normalize = True,
        ),
    scaling = spectra.Scaling(
        xmin = 20,
        xmax = 50,
        ),
    )
aton.plot(ins)
```

"""

from .classes import Spectra, Plotting, Scaling, Material
from . import fit
from . import normalize
from . import deuterium
from . import samples
from .plot import plot

