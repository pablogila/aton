"""
# Physico-chemical constants

This subpackage contains:
- `units`
- `atoms`
- `elements`


Use example:

```python
from aton import phys
phys.eV_to_J  # 1.602176634e-19
phys.atoms['H'].isotope[2].mass  # 2.0141017779
```

"""

from .units import *
from .functions import *
from .atoms import atoms

