"""
# Description

This module contains the `plot()` function,
used to plot `aton.spx.classes.Spectra` data,
containing optional `aton.spx.classes.Plotting` parameters.

It is used as `aton.spx.plot(Spectra)`

---
"""


import matplotlib.pyplot as plt
from .classes import *


def plot(spectra:Spectra):
    """Plots a `spectra`.

    Optional `aton.spectra.classes.Plotting` attributes can be used.
    """
    # To clean the filename
    strings_to_delete_from_name = ['.csv', '.dat', '.txt', '_INS', '_ATR', '_FTIR', '_temp', '_RAMAN', '_Raman', '/data/', 'data/', '/csv/', 'csv/', '/INS/', 'INS/', '/FTIR/', 'FTIR/', '/ATR/', 'ATR/', '_smooth', '_smoothed', '_subtracted', '_cellsubtracted']
    # Avoid modifying the original Spectra object
    sdata = deepcopy(spectra)
    # Matplotlib stuff
    if hasattr(sdata, 'plotting') and sdata.plotting.figsize:
        fig, ax = plt.subplots(figsize=sdata.plotting.figsize)
    else:
        fig, ax = plt.subplots()
    # Optional scaling factor
    scale_factor = sdata.plotting.scaling if hasattr(sdata, 'plotting') and sdata.plotting.scaling else 1.0
    # Calculate Y limits
    calculated_low_ylim, calculated_top_ylim = _get_ylimits(sdata)
    low_ylim = calculated_low_ylim if not hasattr(sdata, 'plotting') or sdata.plotting.ylim[0] is None else sdata.plotting.ylim[0]
    top_ylim = calculated_top_ylim if not hasattr(sdata, 'plotting') or sdata.plotting.ylim[1] is None else sdata.plotting.ylim[1]
    # Get some plotting parameters
    low_xlim = None
    top_xlim = None
    if getattr(sdata, 'plotting', None) is not None:
        title = sdata.plotting.title
        low_xlim = sdata.plotting.xlim[0]
        top_xlim = sdata.plotting.xlim[1]
        xlabel = sdata.plotting.xlabel if sdata.plotting.xlabel is not None else sdata.dfs[0].columns[0]
        ylabel = sdata.plotting.ylabel if sdata.plotting.ylabel is not None else sdata.dfs[0].columns[1]
    else:
        title = sdata.comment
    # Set plot offset
    number_of_plots = len(sdata.dfs)
    height = (top_ylim - low_ylim)
    if hasattr(sdata, 'plotting') and sdata.plotting.offset is True:
        for i, df in enumerate(sdata.dfs):
            reverse_i = (number_of_plots - 1) - i
            df[df.columns[1]] = df[df.columns[1]] + (reverse_i * height / scale_factor)
    elif hasattr(sdata, 'plotting') and (isinstance(sdata.plotting.offset, float) or isinstance(sdata.plotting.offset, int)):
        offset = sdata.plotting.offset
        for i, df in enumerate(sdata.dfs):
            reverse_i = (number_of_plots - 1) - i
            df[df.columns[1]] = df[df.columns[1]] + (reverse_i * offset / scale_factor)
    _, calculated_top_ylim = _get_ylimits(sdata)
    top_ylim = calculated_top_ylim if not hasattr(sdata, 'plotting') or sdata.plotting.ylim[1] is None else sdata.plotting.ylim[1]
    # Set legend
    if hasattr(sdata, 'plotting') and hasattr(sdata.plotting, 'legend'):
        if sdata.plotting.legend == False:
            for df in sdata.dfs:
                df.plot(x=df.columns[0], y=df.columns[1], ax=ax)
        elif sdata.plotting.legend != None:
            if len(sdata.plotting.legend) == len(sdata.dfs):
                for i, df in enumerate(sdata.dfs):
                    if sdata.plotting.legend[i] == False:
                        continue  # Skip plots with False in the legend
                    clean_name = sdata.plotting.legend[i]
                    df.plot(x=df.columns[0], y=df.columns[1], label=clean_name, ax=ax)
            elif len(sdata.plotting.legend) == 1:
                clean_name = sdata.plotting.legend[0]
                for i, df in enumerate(sdata.dfs):
                    df.plot(x=df.columns[0], y=df.columns[1], label=clean_name, ax=ax)
        elif sdata.plotting.legend == None and len(sdata.files) == len(sdata.dfs):
            for df, name in zip(sdata.dfs, sdata.files):
                clean_name = name
                for string in strings_to_delete_from_name:
                    clean_name = clean_name.replace(string, '')
                clean_name = clean_name.replace('_', ' ')
                df.plot(x=df.columns[0], y=df.columns[1], label=clean_name, ax=ax)
    # Matplotlib title and axis, additional margins
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    add_top = 0
    add_low = 0
    if hasattr(sdata, 'plotting'):
        if sdata.plotting.margins and isinstance(sdata.plotting.margins, list):
            add_low = sdata.plotting.margins[0]
            add_top = sdata.plotting.margins[1]
        if sdata.plotting.log_xscale:
            ax.set_xscale('log')
        if not sdata.plotting.show_yticks:
            ax.set_yticks([])
        if sdata.plotting.legend != False:
            ax.legend(title=sdata.plotting.legend_title, fontsize=sdata.plotting.legend_size, loc=sdata.plotting.legend_loc)
        else:
            ax.legend().set_visible(False)
    low_ylim = low_ylim - add_low
    top_ylim = top_ylim + add_top
    ax.set_ylim(bottom=low_ylim)
    ax.set_ylim(top=top_ylim)
    ax.set_xlim(left=low_xlim)
    ax.set_xlim(right=top_xlim)
    # Include optional lines
    if hasattr(sdata, 'plotting') and sdata.plotting.vline is not None and sdata.plotting.vline_error is not None:
        for vline, vline_error in zip(sdata.plotting.vline, sdata.plotting.vline_error):
            lower_bound = vline - vline_error
            upper_bound = vline + vline_error
            ax.fill_between([lower_bound, upper_bound], low_ylim, top_ylim, color='gray', alpha=0.1)
    elif hasattr(sdata, 'plotting') and sdata.plotting.vline is not None:
        for vline in sdata.plotting.vline:
            ax.axvline(x=vline, color='gray', alpha=0.5, linestyle='--')
    # Save the file
    if hasattr(sdata, 'plotting') and sdata.plotting.save_as:
        root = os.getcwd()
        save_name = os.path.join(root, sdata.plotting.save_as)
        plt.savefig(save_name)
    # Show the file
    plt.show()


def _get_ylimits(spectrum:Spectra) -> tuple[float, float]:
    """Private function to obtain the ylimits to plot."""
    # Optional scaling factor
    scale_factor = spectrum.plotting.scaling if hasattr(spectrum, 'plotting') and spectrum.plotting.scaling else 1.0
    # Get the Y limits
    all_y_values = []
    for df in spectrum.dfs:
        df_trim = df
        if hasattr(spectrum, 'plotting') and spectrum.plotting.xlim[0] is not None:
            df_trim = df_trim[(df_trim[df_trim.columns[0]] >= spectrum.plotting.xlim[0])]
        if hasattr(spectrum, 'plotting') and spectrum.plotting.xlim[1] is not None:
            df_trim = df_trim[(df_trim[df_trim.columns[0]] <= spectrum.plotting.xlim[1])]
        all_y_values.extend(df_trim[df_trim.columns[1]].tolist())
    calculated_low_ylim = min(all_y_values)
    calculated_top_ylim = max(all_y_values)
    return calculated_low_ylim, calculated_top_ylim

