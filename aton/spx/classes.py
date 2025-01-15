"""
# Description

This module contains common classes used to load and manipulate spectral data.
Any class can be instantiated directly from the `aton.spx` module,
as `aton.spx.Class()`.


# Index

| | |
| --- | --- |
| `Spectra`  | Used to load and process spectral data |
| `Plotting` | Stores plotting options, used in `Spectra.plotting` |
| `Material` | Used to store and calculate material parameters, such as molar masses and neutron cross sections |


# Examples

To load two INS spectra CSV files with cm$^{-1}$ as input units,
converting them to meV units, and finally plotting them:
```python
from aton import spx
ins = spx.Spectra(
    type     = 'ins',
    files    = ['example_1.csv', 'example_2.csv'],
    units_in = 'cm-1',
    units    = 'meV',
    )
spx.plot(ins)
```

Check more use examples in the [`ATON/examples/`](https://github.com/pablogila/ATON/tree/main/examples) folder.

---
"""


import numpy as np
import pandas as pd
from copy import deepcopy
import os
import aton.st.alias as alias
import aton.phys as phys


class Plotting:
    """Stores plotting options, read by `aton.spx.plot`"""
    def __init__(
            self,
            title:str=None,
            xlim=None,
            ylim=None,
            margins:list=[0,0],
            offset=True,
            scaling:float=1.0,
            vline:list=None,
            vline_error:list=None,
            figsize:tuple=None,
            log_xscale:bool=False,
            show_yticks:bool=False,
            xlabel:str=None,
            ylabel:str=None,
            legend=None,
            legend_title:str=None,
            legend_size='medium',
            legend_loc='best',
            save_as:str=None,
        ):
        """Default values can be overwritten when initializing the Plotting object."""
        self.title = title
        """Title of the plot. Set it to an empty string to remove the title."""
        self.xlim = self._set_limits(xlim)
        """List with the x-limits of the plot, as in `[xlim_low, xlim_top]`."""
        self.ylim = self._set_limits(ylim)
        """List with the y-limits of the plot, as in `[ylim_low, ylim_top]`."""
        self.margins = self._set_limits(margins)
        """List with additional margins at the bottom and top of the plot, as in `[low_margin, top_margin]`."""
        self.offset = offset
        """If `True`, the plots will be separated automatically.

        It can be set to a float, to equally offset the plots by a given value.
        """
        self.scaling = scaling
        "Scaling factor"
        if vline is not None and not isinstance(vline, list):
            vline = [vline]
        self.vline = vline
        """Vertical line/s to plot. Can be an int or float with the x-position, or a list with several ones."""
        if vline_error is not None and not isinstance(vline_error, list):
            vline_error = [vline_error]
        self.vline_error = vline_error
        """Plot a shaded area of the specified width around the vertical lines specified at `vline`.

        It can be an array of the same length as `vline`, or a single value to be applied to all.
        """
        self.figsize = figsize
        """Tuple with the figure size, as in matplotlib."""
        self.log_xscale = log_xscale
        """If true, plot the x-axis in logarithmic scale."""
        self.show_yticks = show_yticks
        """Show or not the yticks on the plot."""
        self.xlabel = xlabel
        """Custom label of the x-axis.

        If `None`, the default label will be used.
        Set to `''` to remove the label of the horizontal axis.
        """
        self.ylabel = ylabel
        """Custom label of the y-axis.
        
        If `None`, the default label will be used.
        Set to `''` to remove the label of the vertical axis.
        """
        if not isinstance(legend, list) and legend is not None and legend != False:
            legend = [legend]
        self.legend = legend
        """Legend of the plot.

        If `None`, the filenames will be used as legend.
        Can be a bool to show or hide the plot legend.
        It can also be an array containing the strings to display;
        in that case, elements set to `False` will not be displayed.
        """
        self.legend_title = legend_title
        """Title of the legend, defaults to `None`."""
        self.legend_size = legend_size
        """Size of the legend, as in matplotlib. Defaults to `'medium'`."""
        self.legend_loc = legend_loc
        """Location of the legend, as in matplotlib. Defaults to `'best'`."""
        self.save_as = save_as
        """Filename to save the plot. None by default."""

    def _set_limits(self, limits) -> list:
        """Set the x and y limits of the plot."""
        if limits is None:
            return [None, None]
        if isinstance(limits, tuple):
            limits = list(limits)
        if isinstance(limits, list):
            if len(limits) == 0:
                return [None, None]
            if len(limits) == 1:
                return [None, limits[0]]
            if len(limits) == 2:
                return limits
            else:
                return limits[:2]
        if isinstance(limits, int) or isinstance(limits, float):
            return [None, limits]
        else:
            raise ValueError(f"Unknown plotting limits: Must be specified as a list of two elements, as [low_limit, high_limit]. Got: {limits}")


class Spectra:
    """Spectra object. Used to load and process spectral data.

    Most functions in the `aton.spx` module receive this object as input.
    """
    def __init__(
            self,
            type:str=None,
            comment:str=None,
            files=None,
            dfs=None,
            units=None,
            units_in=None,
            plotting:Plotting=Plotting(),
        ):
        """All values can be set when initializing the Spectra object."""
        self.type = None
        """Type of the spectra: `'INS'`, `'ATR'`, or `'RAMAN'`."""
        self.comment = comment
        """Custom comment. If `Plotting.title` is None,  it will be the title of the plot."""
        self.files = None
        """List containing the files with the spectral data.

        Loaded automatically to `dfs` with Pandas at initialization.
        In order for Pandas to read the files properly, note that the column lines must start by `#`.
        Any additional line that is not data must be removed or commented with `#`.
        CSV files must be formatted with the first column as the energy or energy transfer,
        and the second column with the intensity or absorbance, depending on the case.
        An additional third `'Error'` column can be used.
        """
        self.dfs = None
        """List containing the pandas dataframes with the spectral data.
        
        Loaded automatically from `files` at initialization.
        """
        self.units = None
        """Target units of the spectral data.
        
        Can be `'meV'` or `'cm-1'`."""
        self.units_in = None
        """Input units of the spectral data, used in the input CSV files.
        
        Can be `'meV'` or `'cm-1'`.
        If the input CSV files have different units,
        it can also be set as a list of the same length of the number of input files,
        eg. `['meV', 'cm-1', 'cm-1']`.
        """
        self.plotting = plotting
        """`Plotting` object, used to set the plotting options."""

        self = self._set_type(type)
        self = self._set_dataframes(files, dfs)
        self = self.set_units(units, units_in)

    def _set_type(self, type):
        """Set and normalize the type of the spectra: `INS`, `ATR`, or `RAMAN`."""
        if type.lower() in alias.experiments['ins']:
            self.type = 'ins'
        elif type.lower() in alias.experiments['atr']:
            self.type = 'atr'
        elif type.lower() in alias.experiments['raman']:
            self.type = 'raman'
        else:
            self.type = type.lower()
        return self

    def _set_dataframes(self, files, dfs):
        '''Set the dfs list of dataframes, from the given files or dfs.'''
        if isinstance(files, list):
            self.files = files
        elif isinstance(files, str):
            self.files = [files]
        else:
            self.files = []

        if isinstance(dfs, pd.DataFrame):
            self.dfs = [dfs]
        elif isinstance(dfs, list) and isinstance(dfs[0], pd.DataFrame):
            self.dfs = dfs
        else:
            self.dfs = [self._read_dataframe(filename) for filename in self.files]
        return self

    def _read_dataframe(self, filename):
        """Read a dataframe from a file."""
        root = os.getcwd()
        file_path = os.path.join(root, filename)
        df = pd.read_csv(file_path, comment='#')
        df = df.sort_values(by=df.columns[0]) # Sort the data by energy

        print(f'\nNew dataframe from {filename}')
        print(df.head(),'\n')
        return df

    def set_units(
            self,
            units,
            units_in=None,
            default_unit='cm-1',
            ):
        """Method to change between spectral units. ALWAYS use this method to do that.

        For example, to change to meV from cm-1:
        ```python
        Spectra.set_units('meV', 'cm-1')
        ```
        """
        mev = 'meV'
        cm = 'cm-1'
        unit_format={
                mev: alias.units['meV'],
                cm: alias.units['cm-1'] + alias.units['cm'],
            }
        if self.units is not None:
            units_in = deepcopy(self.units)
            self.units = units
        elif units is not None:
            units_in = units_in
            self.units = deepcopy(units)
        elif units is None and units_in is None:
            units_in = None
            self.units = default_unit
        elif units is None and units_in is not None:
            units_in = None
            self.units = deepcopy(units_in)
        if isinstance(units_in, list):
            for i, unit_in in enumerate(units_in):
                for key, value in unit_format.items():
                    if unit_in in value:
                        units_in[i] = key
                        break
            if len(units_in) == 1:
                units_in = units_in * len(self.files)
            elif len(units_in) != len(self.files):
                raise ValueError("units_in must be a list of the same length as files.")
        if isinstance(units_in, str):
            for key, value in unit_format.items():
                if units_in in value:
                    units_in = key
                    break
            units_in = [units_in] * len(self.files)
        if isinstance(self.units, list):
            for i, unit in enumerate(self.units):
                for key, value in unit_format.items():
                    if unit in value:
                        self.units[i] = key
                        break
            if len(self.units) == 1:
                self.units = self.units * len(self.files)
            elif len(self.units) != len(self.files):
                raise ValueError("units_in must be a list of the same length as files.")
        if isinstance(self.units, str):
            for key, value in unit_format.items():
                if self.units in value:
                    self.units = key
                    break
            self.units = [self.units] * len(self.files)
        if units_in is None:
            return self
        # Otherwise, convert the dfs
        if len(self.units) != len(units_in):
            raise ValueError("Units len mismatching.")
        for i, unit in enumerate(self.units):
            if unit == units_in[i]:
                continue
            if unit == mev and units_in[i] == cm:
                self.dfs[i][self.dfs[i].columns[0]] = self.dfs[i][self.dfs[i].columns[0]] * phys.cm1_to_meV
            elif unit == cm and units_in[i] == mev:
                self.dfs[i][self.dfs[i].columns[0]] = self.dfs[i][self.dfs[i].columns[0]] * phys.meV_to_cm1
            else:
                raise ValueError(f"Unit conversion error between '{unit}' and '{units_in[i]}'")
        # Rename dataframe columns
        E_units = None
        for i, df in enumerate(self.dfs):
            if self.units[i] == mev:
                E_units = 'meV'
            elif self.units[i] == cm:
                E_units = 'cm-1'
            else:
                E_units = self.units[i]
            if self.type == 'ins':
                if self.dfs[i].shape[1] == 3:
                    self.dfs[i].columns = [f'Energy transfer / {E_units}', 'S(Q,E)', 'Error']
                else:
                    self.dfs[i].columns = [f'Energy transfer / {E_units}', 'S(Q,E)']
            elif self.type == 'atr':
                if self.dfs[i].shape[1] == 3:
                    self.dfs[i].columns = [f'Wavenumber / {E_units}', 'Absorbance', 'Error']
                else:
                    self.dfs[i].columns = [f'Wavenumber / {E_units}', 'Absorbance']
            elif self.type == 'raman':
                if self.dfs[i].shape[1] == 3:
                    self.dfs[i].columns = [f'Raman shift / {E_units}', 'Counts', 'Error']
                else:
                    self.dfs[i].columns = [f'Raman shift / {E_units}', 'Counts']
        return self


class Material:
    """Material class.

    Used to calculate molar masses and cross sections,
    and to pass data to different analysis functions
    such as `aton.spectra.deuterium.impulse_approx().`
    """
    def __init__(
            self,
            elements:dict,
            name:str=None,
            grams:float=None,
            grams_error:float=None,
            mols:float=None,
            mols_error:float=None,
            molar_mass:float=None,
            cross_section:float=None,
            peaks:dict=None,
        ):
        """
        All values can be set when initializing the Material object.
        However, it is recommended to only set the elements and the grams,
        and optionally the name, and calculate the rest with `Material.set()`.
        """
        self.elements = elements
        """Dict of atoms in the material, as in `{'H': 6, 'C':1, 'N':1}`.

        Isotopes can be expressed as 'H2', 'He4', etc. with the atom symbol + isotope mass number.
        """
        self.name = name
        """String with the name of the material."""
        self.grams = grams
        """Mass, in grams."""
        self.grams_error = grams_error
        """Error of the measured mass in grams.

        Set automatically with `Material.set()`.
        """
        self.mols = mols
        """Number of moles.

        Set automatically with `Material.set()`.
        """
        self.mols_error = mols_error
        """Error of the number of moles.

        Set automatically with `Material.set()`.
        """
        self.molar_mass = molar_mass
        """Molar mass of the material, in mol/g.

        Calculated automatically with `Material.set()`.
        """
        self.cross_section = cross_section
        """Neutron total bound scattering cross section, in barns.

        Calculated automatically with `Material.set()`.
        """
        self.peaks = peaks
        """Dict with interesting peaks that you might want to store for later use."""

    def _set_grams_error(self):
        """Set the error in grams, based on the number of decimal places."""
        if self.grams is None:
            return
        decimal_accuracy = len(str(self.grams).split('.')[1])
        # Calculate the error in grams
        self.grams_error = 10**(-decimal_accuracy)

    def _set_mass(self):
        """Set the molar mass of the material.

        If `Material.grams` is provided, the number of moles will be
        calculated and overwritten. Isotopes can be used as 'element + A',
        eg. `'He4'`. This gets splitted with `aton.phys.elements.split_isotope`.
        """
        material_grams_per_mol = 0.0
        for key in self.elements:
            try:
                material_grams_per_mol += self.elements[key] * phys.atoms[key].mass
            except KeyError: # Split the atomic flag as H2, etc
                element, isotope = phys.split_isotope(key)
                material_grams_per_mol += self.elements[key] * phys.atoms[element].isotope[isotope].mass
        self.molar_mass = material_grams_per_mol
        if self.grams is not None:
            self._set_grams_error()
            self.mols = self.grams / material_grams_per_mol
            self.mols_error = self.mols * np.sqrt((self.grams_error / self.grams)**2)
    
    def _set_cross_section(self):
        """Set the cross section of the material, based on the `elements` dict.

        If an isotope is used, eg. `'He4'`, it splits the name with `aton.phys.functions.split_isotope`.
        """
        total_cross_section = 0.0
        for key in self.elements:
            try:
                total_cross_section += self.elements[key] * phys.atoms[key].cross_section
            except KeyError: # Split the atomic flag as H2, etc
                element, isotope_index = phys.split_isotope(key)
                total_cross_section += self.elements[key] * phys.atoms[element].isotope[isotope_index].cross_section
        self.cross_section = total_cross_section

    def set(self):
        """Set the molar mass, cross section and errors of the material."""
        self._set_mass()
        self._set_cross_section()

    def print(self):
        """Print a summary with the material information."""
        print('\nMATERIAL')
        if self.name is not None:
            print(f'Name: {self.name}')
        if self.grams is not None and self.grams_error is not None:
            print(f'Grams: {self.grams} +- {self.grams_error} g')
        elif self.grams is not None:
            print(f'Grams: {self.grams} g')
        if self.mols is not None and self.mols_error is not None:
            print(f'Moles: {self.mols} +- {self.mols_error} mol')
        elif self.mols is not None:
            print(f'Moles: {self.mols} mol')
        if self.molar_mass is not None:
            print(f'Molar mass: {self.molar_mass} g/mol')
        if self.cross_section is not None:
            print(f'Cross section: {self.cross_section} barns')
        if self.elements is not None:
            print(f'Elements: {self.elements}')
        print('')

