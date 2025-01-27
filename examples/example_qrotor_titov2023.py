import aton.qrotor as qr

system = qr.QSys()
system.potential_name = 'titov2023'
system.B = 0.573  # qr.B_CH3
system.E_levels = 10
system.gridsize = 200000

experiment = qr.solve.energies(system)
experiment.comment = 'titov2023'
print('Eigenvalues:')
print(experiment.systems[0].eigenvalues)

print('Rounded eigenvalues:')
precision = 4
for value in experiment.systems[0].eigenvalues:
    print(round(value, precision))

qr.plot.potential(experiment)

