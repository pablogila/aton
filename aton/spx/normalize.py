"""
# Description

This module contains functions to normalize data and other variables.


# Index

| | |
| --- | --- |
| `height()`   | Normalize a `spectra` by height |
| `area()`     | Normalize a `spectra` by the area under the datasets |
| `unit_str()` | Normalize a `unit` string from user input |

---
"""


import aton.alias as alias
from .classes import *
from .fit import *


def height(
        spectra:Spectra,
        range:list=None,
        axis:str='x',
        df_index:int=0,
        ) -> Spectra:
    """Normalize a set of `spectra` by height.

    By default it normalises the spectra over the entire range.
    This can be modified by setting a specific range,
    as in `range = [x_min, x_max]` with `axis = 'x'`.
    It can also normalise over manual y-positions,
    for example for peaks with different baselines.
    This can be done by settingch `axis='y'`, and
    `range = [[y_min_1, y_max_1], ..., [y_min_N, y_max_N]]`.

    Heights are normalised with respect to the
    reference dataframe `df_index`, the first one by default.
    """
    sdata = deepcopy(spectra)
    if axis.lower() in alias.spatial['y']:
        return _height_y(sdata, range, df_index)
    df0 = sdata.dfs[df_index]
    if range:
        if not isinstance(range, list):
            raise ValueError("range must be a list")
        if len(range) != 2:
            raise ValueError(f"With axis='x', range must be [xmin, xmax]. Yours was:\n{range}")
        range.sort()
        xmin = range[0]
        xmax = range[1]
    else:
        xmin = min(df0[df0.columns[0]])
        xmax = max(df0[df0.columns[0]])
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


def _height_y(
        sdata:Spectra,
        range:list,
        df_index:int=0,
        ) -> Spectra:
    """Private function to handle normalisation in the y-axis"""
    if not range:
        raise ValueError(f"A range must be specified to normalise the Y axis, as in range=[[y_min_1,y_max_1],...,[y_min_N,y_max_N]]\nYours was:\n{range}")
    if not len(range) == len(sdata.dfs):
        raise ValueError("len(range) must match len(Spectra.dfs) for axis='y'")
    ymax = []
    ymin = []
    for values in range:
        if not isinstance(values, list):
            raise ValueError(f"The range for axis='y' must be a list of lists,\nas in range=[[y_min_1,y_max_1],...,[y_min_N,y_max_N]].\nYours was:\n{range}")
        if len(values) != 2:
            raise ValueError(f"2 values needed to normalise the y-axis, ymin and ymax,\nas in range=[[y_min_1,y_max_1],...,[y_min_N,y_max_N]].\nYours was:\n{range}")
        values.sort()
        i_ymin = values[0]
        i_ymax = values[1]
        ymin.append(i_ymin)
        ymax.append(i_ymax)
    reference_height = ymax[df_index] - ymin[df_index]
    normalized_dataframes = []
    for i, df in enumerate(sdata.dfs):
        height = ymax[i] - ymin[i]
        df[df.columns[1]] =  df[df.columns[1]] * reference_height / height
        normalized_dataframes.append(df)
    sdata.dfs = normalized_dataframes
    return sdata


def area(
        spectra:Spectra,
        range:list=None,
        df_index:int=0
        ) -> Spectra:
    """Normalize `spectra` by the area under the datasets."""
    sdata = deepcopy(spectra)
    df0 = sdata.dfs[df_index]
    if range:
        if len(range) != 2:
            raise ValueError(f"The range must be a list of 2 elements, as in [xmin, xmax]. Yours was:\n{range}")
        range.sort()
        xmin = range[0]
        xmax = range[1]
    else:
        xmin = min(df0[df0.columns[0]])
        xmax = max(df0[df0.columns[0]])
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


def unit_str(unit:str):
    """Normalize `unit` string from user input."""
    for key, value in alias.units.items():
        if unit in value:
            return key
    print(f"WARNING: Unknown unit '{unit}'")
    return unit

