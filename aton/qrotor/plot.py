"""
# Description

This module provides straightforward functions to plot QRotor data.


# Index

| | |
| --- | --- |
| `potential()`        | Potential values as a function of the angle |
| `energies()`         | Calculated eigenvalues |
| `reduced_energies()` | Reduced energies E/B as a function of the reduced potential V/B |
| `wavefunction()`     | Selected wavefunctions or squared wavefunctions of a system |
| `convergence()`      | Energy convergence |

---
"""


from .system import System
from . import systems
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy


def potential(system:System) -> None:
    """Plot the potential values of a `system`."""
    plt.plot(system.grid, system.potential_values, marker='', linestyle='-')
    plt.xlabel('Angle / rad')
    plt.ylabel('Potential energy / meV')
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
    plt.title(system.comment)
    plt.show()


def energies(data) -> None:
    """Plot the eigenvalues of `data` (System or a list of System objects)."""
    if isinstance(data, System):
        var = [data]
    else:  # Should be a list
        systems.check(data)
        var = data

    V_colors = ['C0'] #...
    E_colors = ['red', 'purple', 'grey']  # To extend...
    E_linestyles = ['--', ':', '-.']
    edgecolors = ['tomato', 'purple', 'grey']

    V_linestyle = '-'
    title = var[0].comment
    ylabel_text = f'Energy / meV'
    xlabel_text = 'Angle / radians'

    plt.figure(figsize=(10, 6))
    plt.xlabel(xlabel_text)
    plt.ylabel(ylabel_text)
    plt.title(title)
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])

    unique_potentials = []
    unique_groups = []
    for i, system in enumerate(var):
        V_color = V_colors[i % len(V_colors)]
        E_color = E_colors[i % len(E_colors)]
        E_linestyle = E_linestyles[i % len(E_linestyles)]
        edgecolor = edgecolors[i % len(edgecolors)]

        # Plot potential energy if it is unique
        if not any(np.array_equal(system.potential_values, value) for value in unique_potentials):
            unique_potentials.append(system.potential_values)
            plt.plot(system.grid, system.potential_values, color=V_color, linestyle=V_linestyle)

        # Plot eigenvalues
        if any(system.eigenvalues):
            text_offset = 3 * len(unique_groups)
            if system.group not in unique_groups:
                unique_groups.append(system.group)
            for j, energy in enumerate(system.eigenvalues):
                plt.axhline(y=energy, color=E_color, linestyle=E_linestyle)
                plt.text(j%3*1.0 + text_offset, energy, f'$E_{{{j}}}$ = {round(energy,4):.04f}', va='top', bbox=dict(edgecolor=edgecolor, boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
            if len(systems.get_groups(var)) > 1:
                plt.plot([], [], color=E_color, label=f'{system.group} Energies')  # Add to legend

    if len(systems.get_groups(var)) > 1:
        plt.subplots_adjust(right=0.85)
        plt.legend(bbox_to_anchor=(1.1, 0.5), loc='center', fontsize='small')

    plt.show()


def reduced_energies(data:list) -> None:
    """Plots the reduced energy of the system E/B vs the reduced potential energy V/B.

    Takes a `data` list of System objects as input.
    """
    systems.check(data)
    number_of_levels = data[0].E_levels
    x = []
    for system in data:
        x.append(system.potential_max_B)
    for i in range(number_of_levels):
        y = []
        for system in data:
            y.append(system.eigenvalues_B[i])
        plt.plot(x, y, marker='', linestyle='-')
    plt.xlabel('V$_{B}$ / B')
    plt.ylabel('E / B')
    plt.title(data[0].comment)
    plt.show()


def wavefunction(system:System, square:bool=True, levels=[0, 1, 2], overlap=False):
    """Plot the wavefunction of a `system` for the specified `levels`.

    Wavefunctions are squared by default, showing the probabilities;
    To show the actual wavefunctions, set `square = False`.

    `levels` can be a list of indexes, or the number of levels to plot.

    Specific wavefunctions can be overlapped with `overlap` as a list with the target indexes.
    The `overlap` value can also be the max number of wavefunctions to add.
    All found wavefunctions can be added together with `overlap = True`;
    but note that this overlap is limited by the number of System.E_levels,
    that must be specified before solving the system.
    Setting `overlap` will ignore the `levels` argument.
    """
    data = deepcopy(system)
    eigenvectors = data.eigenvectors

    title = data.comment
    fig, ax1 = plt.subplots()
    plt.title(title)
    ax1.set_xlabel('Angle / radians')
    ax1.set_ylabel('Potential / meV')
    ax1.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
    ax1.plot(data.grid, data.potential_values, color='blue', linestyle='-')
    ax2 = ax1.twinx()
    ax2.set_yticks([])
    ax2.set_ylabel('Squared wavefunction' if square else 'Wavefunction')

    # Set levels list
    if isinstance(levels, int) or isinstance(levels, float):
        levels = [x for x in range(int(levels))]
    if not isinstance(levels, list):
        raise ValueError('levels must be an int or a list of ints')
    # Set overlap if requested
    if overlap == True and isinstance(overlap, bool):
        eigenvectors = [np.sum(eigenvectors, axis=0)]
        levels = [0]
        show_legend = False
    elif overlap is not False and (isinstance(overlap, int) or isinstance(overlap, float)):
        max_int = int(overlap)
        eigenvectors = [np.sum(eigenvectors[:max_int], axis=0)]
        levels = [0]
        show_legend = False
    elif isinstance(overlap, list):
        eigenvectors = [np.sum([eigenvectors[i] for i in overlap], axis=0)]
        levels = [0]
        show_legend = False
    else:
        show_legend = True
    # Square values if so
    if square:
        eigenvectors = [vec**2 for vec in eigenvectors]
    # Plot the wavefunction
    for i in levels:
        ax2.plot(data.grid, eigenvectors[i], linestyle='--', label=f'{i}')
    if show_legend:
        fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.88), fontsize='small', title='Index')

    plt.show()


def convergence(data:list) -> None:
    """Plot the energy convergence of a `data` list of Systems as a function of the gridsize."""
    systems.check(data)
    gridsizes = [system.gridsize for system in data]
    runtimes = [system.runtime for system in data]
    deviations = []  # List of lists, containing all eigenvalue deviations for every system
    E_levels = data[0].E_levels
    for system in data:
        deviation_list = []
        for i, eigenvalue in enumerate(system.eigenvalues):
            ideal_E = systems.get_ideal_E(i)
            deviation = abs(ideal_E - eigenvalue)
            deviation_list.append(deviation)
        deviation_list = deviation_list[1:]  # Remove ground state
        deviations.append(deviation_list)
    # Plotting
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Grid size')
    ax1.set_ylabel('Error / meV')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Runtime / s')
    ax2.set_yscale('log')
    ax2.plot(gridsizes, runtimes, color='tab:grey', label='Runtime', linestyle='--')
    colors = plt.cm.viridis(np.linspace(0, 1, E_levels-1))
    for i in range(E_levels-1):
        if i % 2 == 0:  # Ignore even numbers, since those levels are degenerated.
            continue
        ax1.plot(gridsizes, [dev[i] for dev in deviations], label=f'$E_{{{int((i+1)/2)}}}$', color=colors[i])
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.88), fontsize='small')
    plt.title(data[0].comment if data[0].comment else 'Energy convergence vs grid size')
    plt.show()

