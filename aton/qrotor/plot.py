"""
# Description

This module provides straightforward functions to plot QRotor data.


# Index

| | |
| --- | --- |
| `reduced_energies()` | Reduced energies E/B as a function of the reduced potential V/B |
| `potential()`        | Potential values as a function of the angle |
| `energies()`         | Calculated eigenvalues |
| `convergence()`      | Energy convergence |
| `eigenvectors_DEV()` | NOT IMPLEMENTED |

---
"""


from .system import System
from . import systems
import matplotlib.pyplot as plt
import numpy as np


def reduced_energies(data:list) -> None:
    """Plots the reduced energy of the system E/B vs the reduced potential energy V/B.

    Takes a list of System objects as input.
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


def potential(system:System) -> None:
    """Plot the potential values of a `system`."""
    plt.plot(system.grid, system.potential_values, marker='', linestyle='-')
    plt.xlabel('Angle / rad')
    plt.ylabel('Potential energy / meV')
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
    plt.title(system.comment)
    plt.show()


def energies(data) -> None:
    """Plot the eigenvalues of `var` (System or a list of System objects)."""
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
        if system.eigenvalues is not None:
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


def convergence(data:list) -> None:
    """Plot the energy convergence of a list of Systems as a function of the gridsize."""
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
    ax2.set_ylabel('Runtime [s]')
    ax2.set_yscale('log')
    ax2.plot(gridsizes, runtimes, color='tab:red', label='Runtime', linestyle='--')
    for i in range(E_levels-1):
        if i % 2 == 0:  # Ignore even numbers, since those levels are degenerated.
            continue
        ax1.plot(gridsizes, [dev[i] for dev in deviations], label=f'$E_{int((i+1)/2)}$')
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.88), fontsize='small')
    plt.title(data[0].comment if data[0].comment else 'Energy convergence vs gridsize')
    plt.show()


##  TODO: Implement the following functions


def eigenvectors_DEV(data:System, levels=None, squared=False, scaling_factor=1):

    xlabel = 'Angle / radians'
    ylabel = 'Energy / meV'
    title = data.title
    V_color = 'lightblue'
    V_label = 'Potential'

    #energy_color = 'red'
    energy_edgecolor = 'lightgrey'
    energy_linestyle = ':'
    energy_label = 'E'

    eigenvector_linestyle = '--'

    # To square the eigenvectors
    if squared:
        eigenvector_label = 'Eigenvect$^2$ '
        square = 2
    else:
        eigenvector_label = 'Eigenvect '
        square = 1
    
    for i, potential in enumerate(data.set_of_potentials):

        # Transpose the 2D array so that each inner array represents a different eigenvector
        eigenvectors_transposed = np.transpose(data.set_of_eigenvectors[i])

        # Plot potential energy
        plt.figure(figsize=(10, 6))
        plt.plot(data.x, potential, color=V_color, label=V_label)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(f'{title} (#' + str(i+1) + ')' )
        if len(data.set_of_potentials) == 1:
            plt.title(f'{title}')
        plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
                   ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
        for j, energy in enumerate(data.set_of_energies[i]):
            if levels is not None and j not in levels:
                continue

            color = 'C' + str(j)

            E_label = energy_label + str(j)
            plt.axhline(y=energy, linestyle=energy_linestyle, color=color, label=E_label)
            plt.text(j%3*0.9, energy, f'E$_{j}$ = {energy:.4f}', va='top', bbox=dict(edgecolor=energy_edgecolor, boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

            eigenvect_label = eigenvector_label + str(j)
            eigenvector = scaling_factor*eigenvectors_transposed[j]**square
            plt.plot(data.x, eigenvector, linestyle=eigenvector_linestyle, label=eigenvect_label, color=color)

        plt.subplots_adjust(right=0.85)
        plt.legend(bbox_to_anchor=(1.1, 0.5), loc='center', fontsize='small')
        plt.text(1.03, 0.9, f'Eigenvects\nscaled x{scaling_factor}', transform=plt.gca().transAxes)
        plt.show()



