"""
# Description

This module is used to solve the hamiltonian eigenvalues and eigenvectors for a given quantum system.
Sparse matrices are used to achieve optimal performance.


# Index

| | |
| --- | --- |
| `energies()`              | Solve the system(s) for the `QSys` or `QExp` object |
| `potential()`             | Solve the potential values of the system |
| `schrodinger()`           | Solve the Schrödiger equation for the system |
| `hamiltonian_matrix()`    | Calculate the hamiltonian matrix of the system |
| `laplacian_matrix()`      | Calculate the second derivative matrix for a given grid |

---
"""


from .classes import *
from .potential import solve as solve_potential
from .potential import interpolate
from copy import deepcopy
import time
import numpy as np
from scipy import sparse
import aton


def energies(var, filename:str=None) -> QExp:
    """Solves the Schrödinger equation for a given `var` (`QSys` or `QExp` object).

    The resulting `QExp` object is saved to `filename` if specified.
    """
    if isinstance(var, QSys):
        data = QExp()
        data.systems = [deepcopy(var)]
        data.comment = var.comment
    elif isinstance(var, QExp):
        data = deepcopy(var)
    else:
        raise TypeError('Input must be a QSys or QExp object.')
    for system in data.systems:
        if not any(system.grid):
            system.set_grid()
        system = potential(system)
        system = schrodinger(system)
    if filename:
        aton.st.file.save(data, filename)
    return data


def potential(system:QSys) -> QSys:
    """Solves the potential_values of the system.

    It interpolates the potential if `system.gridsize` is larger than the current grid.
    It solves the potential according to the potential name,
    by calling `aton.qrotor.potential.solve`.
    Then it applies extra operations, such as removing the potential offset
    if `aton.qrotor.classes.QSys.correct_potential_offset = True`.
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


def schrodinger(system:QSys) -> QSys:
    """Solves the Schrödinger equation for a given `aton.qrotor.classes.QSys` object.
    
    Uses ARPACK in shift-inverse mode to solve the hamiltonian sparse matrix.
    """
    time_start = time.time()
    V = system.potential_values
    H = hamiltonian_matrix(system)
    print('Solving Hamiltonian matrix...')
    # Solve eigenvalues with ARPACK in shift-inverse mode, with a sparse matrix
    eigenvalues, eigenvectors = sparse.linalg.eigsh(H, system.E_levels, which='LM', sigma=0, maxiter=10000)
    if any(eigenvalues) is None:
        print('WARNING:  Not all eigenvalues were found.\n')
    else: print('Done.')
    system.runtime = time.time() - time_start
    system.eigenvalues = eigenvalues
    system.potential_max = max(V)
    system.potential_min = min(V)
    system.energy_barrier = max(V) - min(eigenvalues)
    system.first_transition = eigenvalues[1] - eigenvalues[0]
    if system.save_eigenvectors == True:
        system.eigenvectors = eigenvectors
    system.eigenvalues_B = eigenvalues / system.B
    system.potential_max_B = system.potential_max / system.B
    return system


def hamiltonian_matrix(system:QSys):
    """Calculates the Hamiltonian matrix for a given `aton.qrotor.classes.QSys` object."""
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

