import aton.spx as spx
from pytest import approx


folder = 'tests/samples/'
example_csv = folder + 'example_spx_2.02g.csv'
example_csv_nd = folder + 'example_spx_ND_1.284g.csv'


def test_spectra():
    # Define the Spectra data and Plotting options
    ins = spx.Spectra(
        type     = 'INS',
        files    = [example_csv, example_csv_nd],
        units_in = 'cm1',
        units    = 'meV',
        plotting = spx.Plotting(
            title      = 'Example spectra',
            xlim       = [8, 1000],
            offset     = True,
            scaling    = 0.9,
            margins    = [0.2, 0.2],
            xlabel     = 'Energy / meV',
            ylabel     = 'S(Q,E)',
            legend     = ['example 1', 'example 2'],
            log_xscale = True,
        ),
    )
    assert ins.units == ['meV', 'meV']
    assert ins.type == 'ins'


def test_normalize():
    # Define the Spectra data and Plotting options
    ins = spx.Spectra(
        type     = 'ins',
        files    = [example_csv, example_csv_nd],
        units_in = 'cm-1',
        units    = 'meV',
        plotting = spx.Plotting(
            title      = 'Example spectra',
            xlim       = [8, 1000],
            offset     = True,
            scaling    = 0.9,
            margins    = [0.2, 0.2],
            xlabel     = 'Energy / meV',
            ylabel     = 'S(Q,E)',
            legend     = ['example 1', 'example 2'],
            log_xscale = True,
        ),
    )
    # Normalise the spectra to the same height in a given range
    normalization_range = [5, 500]
    ins = spx.normalize.height(spectra=ins, range=normalization_range)
    # The full range was not normalised
    assert max(ins.dfs[0]['S(Q,E)']) != max(ins.dfs[1]['S(Q,E)'])
    # The normalised range should have the same max
    trimmed_dfs = []
    for df in ins.dfs:
        df = df[(df[df.columns[0]] >= normalization_range[0])]
        df = df[(df[df.columns[0]] <= normalization_range[1])]
        trimmed_dfs.append(df)
    ins.dfs = trimmed_dfs
    assert max(ins.dfs[0]['S(Q,E)']) == max(ins.dfs[1]['S(Q,E)'])


def test_fit():
    ins = spx.Spectra(
        type     = 'ins',
        files    = [example_csv, example_csv_nd],
        units_in = 'cm-1',
        units    = 'meV',
    )
    plateau, plateau_error = spx.fit.plateau(spectra=ins, cuts=[33, 36])
    assert float(plateau) == approx(0.14, abs=0.01)
    assert float(plateau_error) == approx(0.01, abs=0.01)
    area, area_error = spx.fit.area_under_peak(spectra=ins, peak=[36, 39, plateau, plateau_error])
    assert float(area) == approx(1.12, abs=0.02)
    assert float(area_error) == approx(0.02, abs=0.01)

