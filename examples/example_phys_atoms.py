from aton import phys

print('We can extract atomic masses with the atom megadict, as atoms[symbol].mass')
H_mass = phys.atoms['H'].mass
print(f'  Hydrogen mass is:  {H_mass} uma')

print('We can access isotope data such as the cross section with maat.atom[symbol].isotope[A].cross_section')
D_cross_section = phys.atoms['H'].isotope[2].cross_section
print(f'  Total bound scattering cross section for D is: {D_cross_section}')

print("Let's see what isotopes are available for helium, with phys.allowed_isotopes(symbol):")
He_isotopes = phys.allowed_isotopes('He')
print(f"  {He_isotopes}")

print("We can also split the name of an isotope into its element and mass number, with phys.split_isotope(isotope):")
He4 = 'He4'
element, isotope = phys.split_isotope(He4)
print(f"  {He4} was splitted to {element} + {isotope}")

print('More info in the docs!')
He3_mass = phys.atoms['He'].isotope[3].mass
He4_mass = phys.atoms['He'].isotope[4].mass
He3_abundance = phys.atoms['He'].isotope[3].abundance
He4_abundance = phys.atoms['He'].isotope[4].abundance
print(f'  He3 mass is: {He3_mass} uma ({He3_abundance} abundance)')
print(f'  He4 mass is: {He4_mass} uma ({He4_abundance} abundance)')

