"""
This script is used to calculate and plot the energy convergence as a function of the grid size.
"""


import aton.qrotor as qr


E_levels_to_calculate = 15  # Note that E levels will be degenerated!
gridsizes = [100, 200, 500, 1000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]

systems = []
for gridsize in gridsizes:
    system = qr.System()
    system.potential_name = 'zero'
    system.B = 1
    system.E_levels = E_levels_to_calculate
    system.gridsize = gridsize
    system.solve()
    systems.append(system)

qr.plot.convergence(systems)

