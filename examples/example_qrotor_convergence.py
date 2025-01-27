import aton.qrotor as qr

system = qr.QSys()
system.potential_name = 'zero'
system.B = 1
system.E_levels = 10
system.gridsize = 200000

experiment = qr.solve.energies(system)
print('Eigenvalues:')
print(experiment.systems[0].eigenvalues)

print('Rounded eigenvalues:')
precision = 4
for value in experiment.systems[0].eigenvalues:
    print(round(value, precision))

