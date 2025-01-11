"""
# Description

This module contains spectral analysis tools.


# Index

| | |
| --- | --- |
| `aton.spx.classes`   | Definition of the `Spectra`, `Plotting`, `Scaling` and `Material` classes, instantiated as `aton.spx.Class()` |
| `aton.spx.fit`       | Spectral fitting functions |
| `aton.spx.normalize` | Spectra normalisation |
| `aton.spx.deuterium` | Deuteration estimation functions |
| `aton.spx.samples`   | Material definition examples |
| `aton.spx.plot`      | Spectra plotting, as `spectra.plot(Spectra)` |


# Examples

To load two INS spectra CSV files with cm$^{-1}$ as input units,
and plot them in meV units, normalizing their heights over the range from 20 to 50 meV:
```python
from aton import spx
plotting_options = spx.Plotting(
    title     = 'Calculated INS',
    normalize = True,
)
scaling_options = spx.Scaling(
    xmin = 20,
    xmax = 50,
)
ins = spx.Spectra(
    type     = 'INS',
    files    = ['example_1.csv', 'example_2.csv'],
    units_in = 'cm-1',
    units    = 'meV',
    plotting = plotting_options
    scaling  = scaling_options
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

