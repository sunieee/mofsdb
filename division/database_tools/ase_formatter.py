from ase.io import read, write
import os

# cif_path = '../mt/output'
# out_path = '../mt/formatter'

cif_path = '../data/1'
out_path = '../data/11'

os.makedirs(out_path, exist_ok=True)

for cif in os.listdir(cif_path):
    mof = read(os.path.join(cif_path, cif))

    write(os.path.join(out_path, cif), mof)

