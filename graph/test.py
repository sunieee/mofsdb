from ase.io import read, write
import ccdc


# cif = read('example/ABEFUL.cif')

entry = ccdc.entry.Entry()
entry.from_string('example/ABEFUL.cif', format='cif')


with open('example/ABEFUL.mol', "w") as f:
    f.write(entry.to_string("mol"))

    