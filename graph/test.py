from ase.io import read, write
import ccdc


cif = read('example/ABEFUL.cif')
write('example/ABEFUL.mol', cif)

