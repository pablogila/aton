"""
# Description

This module contains spectral analysis tools.

# Index

- `aton.spectra.classes`
- `aton.spectra.fit`
- `aton.spectra.normalize`
- `aton.spectra.deuterium`
- `aton.spectra.samples`
- `aton.spectra.plot`

"""

from .classes import Spectra, Plotting, Scaling, Material
from . import fit
from . import normalize
from . import deuterium
from . import samples
from .plot import plot

