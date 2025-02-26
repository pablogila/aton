"""
# Description

This module is used to solve any given quantum system.

Although the functions of this module can be used independently,
it is highly recommended to use the `System.solve()` method instead,
which does all the solving automatically (see `aton.qrotor.system.System.solve()`).
However, advanced users might want to use some of these functions independently;
for example, if your system energy levels are not degenerated in triplets,
you might want to use `excitations()` to solve the energy excitations and tunnel splittings with the proper degeneracy.


# Index

| | |
| --- | --- |
| `energies()`              | Solve the quantum system, including eigenvalues and eigenvectors |
| `potential()`             | Solve the potential values of the system |
| `schrodinger()`           | Solve the Schrödiger equation for the system |
| `hamiltonian_matrix()`    | Calculate the hamiltonian matrix of the system |
| `laplacian_matrix()`      | Calculate the second derivative matrix for a given grid |
| `excitations()`           | Get excitation levels and tunnel splitting energies for a set of eigenvalues |

---
"""


from .system import System
from .potential import solve as solve_potential
from .potential import interpolate
import time
import numpy as np
from scipy import sparse
import aton
from aton._version import __version__


def energies(system:System, filename:str=None) -> System:
    """Solves the quantum `system`.

    This includes solving the potential, the eigenvalues and the eigenvectors.

    The resulting System object is saved with pickle to `filename` if specified.
    """
    if not any(system.grid):
        system.set_grid()
    system = potential(system)
    system = schrodinger(system)
    if filename:
        aton.st.file.save(system, filename)
    return system


def potential(system:System) -> System:
    """Solves the potential values of the `system`.

    It interpolates the potential if `system.gridsize` is larger than the current grid.
    It solves the potential according to the potential name,
    by calling `aton.qrotor.potential.solve()`.
    Then it applies extra operations, such as removing the potential offset
    if `system.correct_potential_offset = True`.
    """
    if system.gridsize and any(system.grid):
        if system.gridsize > len(system.grid):
            system = interpolate(system)
    V = solve_potential(system)
    if system.correct_potential_offset is True:
        offset = min(V)
        V = V - offset
        system.potential_offset = offset
    system.potential_values = V
    return system


def schrodinger(system:System) -> System:
    """Solves the Schrödinger equation for a given `system`.
    
    Uses ARPACK in shift-inverse mode to solve the hamiltonian sparse matrix.
    """
    time_start = time.time()
    V = system.potential_values
    H = hamiltonian_matrix(system)
    print('Solving Schrodinger equation...')
    # Solve eigenvalues with ARPACK in shift-inverse mode, with a sparse matrix
    eigenvalues, eigenvectors = sparse.linalg.eigsh(H, system.E_levels, which='LM', sigma=0, maxiter=10000)
    if any(eigenvalues) is None:
        print('WARNING:  Not all eigenvalues were found.\n')
    else: print('Done.')
    system.version = __version__
    system.runtime = time.time() - time_start
    system.eigenvalues = eigenvalues
    system.potential_max = max(V)
    system.potential_min = min(V)
    system.energy_barrier = max(V) - min(eigenvalues)
    # Solve excitations and tunnel splittings, assuming triplet degeneracy
    system = excitations(system, deg=3)
    # Do we really need to save eigenvectors?
    if system.save_eigenvectors == True:
        system.eigenvectors = np.transpose(eigenvectors)
    return system


def hamiltonian_matrix(system:System):
    """Calculates the Hamiltonian sparse matrix for a given `system`."""
    print(f'Creating Hamiltonian matrix of size {system.gridsize}...')
    V = system.potential_values.tolist()
    potential = sparse.diags(V, format='lil')
    B = system.B
    x = system.grid
    H = -B * laplacian_matrix(x) + potential
    return H


def laplacian_matrix(grid):
    """Calculates the Laplacian (second derivative) matrix for a given `grid`."""
    x = grid
    diagonals = [-2*np.ones(len(x)), np.ones(len(x)), np.ones(len(x))]
    laplacian_matrix = sparse.spdiags(diagonals, [0, -1, 1], format='lil')
    # Periodic boundary conditions
    laplacian_matrix[0, -1] = 1
    laplacian_matrix[-1, 0] = 1
    dx = x[1] - x[0]
    laplacian_matrix /= dx**2
    return laplacian_matrix


def excitations(
        system:System,
        deg:int=3,
        ) -> tuple:
    """Calculate the excitation levels and the tunnel splitting energies of a system.

    Stops the calculation when energies reach the maximum potential.
    Assumes that eigenvalues are degenerated in triplets;
    this degeneracy can be specified with `deg`.
    """
    eigenvalues = system.eigenvalues
    V_max = system.potential_max
    ground_energy = min(eigenvalues)
    excitations = []
    tunnel_splittings = []
    i = 0
    while (i + deg-1) <= len(eigenvalues):
        # Get the eigenvalues corresponding to this triplet (or whatever degeneracy)
        i_max = i + deg  # Index indicating the end of this triplet
        triplet = eigenvalues[i:i_max]
        # Check that we are still below the potential max
        if any(triplet) > V_max:
            break
        # Check that all eigenvalues are valid, and not None
        if any(triplet) is None:
            break
        # Get the excitation energy, by comparing with the ground state
        if i != 0:  # Skip the ground energy level
            excitations.append(min(triplet) - ground_energy)
        # Check the energy differences inside each triplet (or whatever degeneracy)
        E_diff = []
        for j in range(deg-1):  # 0, 1 (not 2)
            E_0 = triplet[j]
            E_1 = triplet[j+1]
            diff = E_1 - E_0
            E_diff.append(diff)
        # Get the maximum energy difference inside the triplet, which is the tunnel splitting
        tunnel_splittings.append(max(E_diff))
        # Move to the next triplet
        i += deg
    # Set the energy excitations and tunnel splittings
    system.excitations = excitations
    system.splittings = tunnel_splittings
    return system

