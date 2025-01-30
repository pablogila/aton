import aton.qrotor as qr

# Testing convergence for a specific energy level
E_level = 5
gridsize = 200000

# Definition of the quantum system for a zero potential
system = qr.System()
system.potential_name = 'zero'
system.B = 1  # Rotational inertia
system.E_levels = 10  # Number of energy levels to calculate
system.gridsize = gridsize
# Solve the system eigenvalues
system = qr.solve.energies(system)
print(f'Eigenvalues: {system.eigenvalues}')
# Compare the calculated and ideal energies
ideal_E = system.get_ideal_E(E_level)
real_E = system.eigenvalues[E_level]
deviation = abs(ideal_E - real_E)
print(f'Deviation from ideal energy for the eigenvalue #{E_level} with a grid of size {gridsize}: {deviation} meV')

