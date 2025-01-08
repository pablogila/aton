"""
# Description
This module contains functions to normalize data and other variables.

# Index
- `unit_str()`
- `spectra()`
- `area()`

---
"""


import aton.st.alias as alias
from .classes import *
from .fit import *


def unit_str(unit:str):
    """Normalize `unit` string from user input."""
    for key, value in alias.units.items():
        if unit in value:
            return key
    print(f"WARNING: Unknown unit '{unit}'")
    return unit


def height(spectra:Spectra):
    """Normalize a `spectra` by height

    Optional `aton.spectra.classes.Scaling` attributes can be used.
    """
    sdata = deepcopy(spectra)
    if hasattr(sdata, 'scaling') and sdata.scaling is not None:
        scaling = sdata.scaling
        if scaling.ymax:
            return _height_y(sdata)
    else:
        scaling = Scaling()

    df_index = scaling.index if scaling.index else 0
    df0 = sdata.dfs[df_index]

    if scaling.xmin is None:
        scaling.xmin = min(df0[df0.columns[0]])
    if scaling.xmax is None:
        scaling.xmax = max(df0[df0.columns[0]])

    sdata.scaling = scaling

    xmin = scaling.xmin
    xmax = scaling.xmax

    df0 = df0[(df0[df0.columns[0]] >= xmin) & (df0[df0.columns[0]] <= xmax)]
    ymax_on_range = df0[df0.columns[1]].max()
    normalized_dataframes = []
    for df in sdata.dfs:
        df_range = df[(df[df.columns[0]] >= xmin) & (df[df.columns[0]] <= xmax)]
        i_ymax_on_range = df_range[df_range.columns[1]].max()
        df[df.columns[1]] =  df[df.columns[1]] * ymax_on_range / i_ymax_on_range
        normalized_dataframes.append(df)
    sdata.dfs = normalized_dataframes
    return sdata


def _height_y(sdata:Spectra):
    """Private function to handle ``"""
    if not len(sdata.scaling.ymax) == len(sdata.dfs):
        raise ValueError("normalize: len(ymax) does not match len(dataframe)")
    scaling = sdata.scaling
    ymax = scaling.ymax
    ymin = scaling.ymin if scaling.ymin else [0.0]
    if len(ymin) == 1:
        ymin = ymin * len(sdata.dfs)
    index = scaling.index if scaling.index else 0
    reference_height = ymax[index] - ymin[index]
    normalized_dataframes = []
    for i, df in enumerate(sdata.dfs):
        height = ymax[i] - ymin[i]
        df[df.columns[1]] =  df[df.columns[1]] * reference_height / height
        normalized_dataframes.append(df)
    sdata.dfs = normalized_dataframes
    return sdata


def area(spectra:Spectra):
    """Normalize `spectra` by the area under the datasets.
 
    Optional `aton.spectra.classes.Scaling` attributes can be used.
    """
    sdata = deepcopy(spectra)
    if hasattr(sdata, 'scaling') and sdata.scaling is not None:
        scaling = sdata.scaling
        if scaling.ymax:
            return _normalize_y(sdata)
    else:
        scaling = Scaling()

    df_index = scaling.index if scaling.index else 0
    df0 = sdata.dfs[df_index]

    if scaling.xmin is None:
        scaling.xmin = min(df0[df0.columns[0]])
    if scaling.xmax is None:
        scaling.xmax = max(df0[df0.columns[0]])

    sdata.scaling = scaling

    xmin = scaling.xmin
    xmax = scaling.xmax

    df0 = df0[(df0[df0.columns[0]] >= xmin) & (df0[df0.columns[0]] <= xmax)]
    area_df0, _ = area_under_peak(sdata, peak=[xmin,xmax], df_index=df_index, min_as_baseline=True)
    normalized_dataframes = []
    for df_i, df in enumerate(sdata.dfs):
        area_df, _ = area_under_peak(sdata, peak=[xmin,xmax], df_index=df_i, min_as_baseline=True)
        scaling_factor = area_df0 / area_df
        df[df.columns[1]] =  df[df.columns[1]] * scaling_factor
        normalized_dataframes.append(df)
    sdata.dfs = normalized_dataframes
    return sdata

