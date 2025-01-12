"""
# Description

This module contains premade examples of material compositions, for testing purposes.
The `aton.spx.classes.Material.grams` is yet to be provided,
before setting the material as `aton.spx.Material.set()`.

---
"""


from .classes import Material


CH3NH3PbI3 = Material(
    elements={'Pb': 1, 'I': 3, 'C': 1, 'N': 1, 'H': 6},
    name='MAPbI3'
    )
"""CH$_3$NH$_3$PbI$_3$"""


CD3ND3PbI3 = Material(
    elements={'Pb': 1, 'I': 3, 'C': 1, 'N': 1, 'H2': 6},
    name='CD3ND3PbI3',
    peaks = {
        'baseline'       : 0.057,  # IREPA-ND-02
        'baseline_error' : 0.008,
        'h6d0'           : [36.0, 39.0],
        'h5d1'           : [33.0, 35.0],
        'h4d2'           : [30.7, 33.0],
        'h3d3'           : [28.8, 30.7],
    },
)
"""CD$_3$ND$_3$PbI$_3$.

With experimental values of the partially-deuterated amine peaks
for the disrotatory mode of MAPbI3's methylammonium.
Measured at TOSCA, ISIS RAL, UK, May 2024.
"""


CH3ND3PbI3 = Material(
    elements={'Pb': 1, 'I': 3, 'C': 1, 'N': 1, 'H': 3, 'H2': 3},
    name='CH3ND3PbI3',
    peaks = {
        'baseline'       : 0.057,  # IREPA-ND-02
        'baseline_error' : 0.008,
        'h6d0'           : [36.0, 39.0],
        'h5d1'           : [33.0, 35.0],
        'h4d2'           : [30.7, 33.0],
        'h3d3'           : [28.8, 30.7],
    },
)
"""CH$_3$ND$_3$PbI$_3$.

With experimental values of the partially-deuterated amine peaks
for the disrotatory mode of MAPbI3's methylammonium.
Measured at TOSCA, ISIS RAL, UK, May 2024.
"""
#MAPI_ND.set()


CD3NH3PbI3 = Material(
    elements={'Pb': 1, 'I': 3, 'C': 1, 'N': 1, 'H': 3, 'H2': 3},
    name='CD3NH3PbI3',
)
"""CD$_3$NH$_3$PbI$_3$"""
#MAPI_CD.set()


CH3NH3I = Material(
    elements={'C' : 1, 'N': 1, 'H': 6},
    name='CH3NH3'
)
"""CH$_3$NH$_3$I"""
#CH3NH3I.set()


CH3ND3I = Material(
    elements={'C' : 1, 'N': 1, 'H': 3, 'H2': 3},
    name='CH3ND3'
)
"""CH$_3$ND$_3$I"""
#CH3ND3I.set()

