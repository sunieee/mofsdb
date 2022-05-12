from turtle import distance
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import pandas as pd
import re
import os
import datetime


rate = 40

class Atom:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if 'mol' in self.__dict__:
            x, y, z, self.t = self.mol.split()[:4]
            self.x = round(float(x)/rate, 5)
            self.y = round(float(y)/rate, 5)
            self.z = round(float(z)/rate, 5)

    @property
    def name(self):
        return f"{self.t}{self.id}"

    def cif(self):
        return "{:7}{:6}{:9}{:9}{:9}  0.00000  Uiso   1.00".format(self.name, self.t, self.x, self.y, self.z)

    def distance(self, atom):
        return round(((self.x - atom.x) ** 2 + (self.y - atom.y) ** 2 + (self.z - atom.z) ** 2) ** 0.5, 5)


class Bond:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if 'mol' in self.__dict__:
            a, b, t = self.mol.split()[:3]
            self.a = int(a) - 1
            self.b = int(b) - 1
            self.t = {'1': 'S',
                '2': 'D',
                '3': 'T'}[t]

    def cif(self, atoms):
        a = atoms[self.a]
        b = atoms[self.b]
        return "{:7}{:7}{:9}  .   {}".format(a.name, b.name, a.distance(b), self.t)


def mol2cif(mol_path, cif_path=None):
    if cif_path is None:
        cif_path = mol_path.replace('.mol', '.cif')
    tmp_path = mol_path.replace('.mol', '.txt')

    mol = Chem.MolFromMolFile(mol_path)
    m2 = Chem.AddHs(mol) # 加氢原子
    AllChem.EmbedMolecule(m2) # 2D->3D化
    AllChem.MMFFOptimizeMolecule(m2)   # 使用MMFF94最小化RDKit生成的构象
    #m3 = Chem.RemoveHs(m2) # 删除氢原子
    #print(Chem.MolToMolBlock(m3))
    m2.SetProp('_Name', 'cyclobutane')
    Chem.MolToMolFile(m2, tmp_path)

    with open(tmp_path,'r',encoding='utf-8') as f:
        cas_lines=f.readlines()
    atoms = []
    bonds = []
    for line in cas_lines:
        if line.count('0  0  0  0  0  0  0  0  0  0  0  0'):
            atoms.append(Atom(mol=line, id=len(atoms)+1))
        elif re.findall(r'[A-Za-z]', line) or len(line.strip())==0:
            pass
        else:
            bonds.append(Bond(mol=line))
    os.remove(tmp_path)
    print(atoms, bonds)

    s = f'''data_cif_{os.path.split(mol_path)[-1]}
_audit_creation_date              {datetime.date.today()}
_audit_creation_method            'Materials Studio'
_symmetry_space_group_name_H-M    'P1'
_symmetry_Int_Tables_number       1
_symmetry_cell_setting            triclinic
loop_
_symmetry_equiv_pos_as_xyz
  x,y,z
_cell_length_a                    {rate}.0000
_cell_length_b                    {rate}.0000
_cell_length_c                    {rate}.0000
_cell_angle_alpha                 90.0000
_cell_angle_beta                  90.0000
_cell_angle_gamma                 90.0000
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_adp_type
_atom_site_occupancy
''' + '\n'.join([x.cif() for x in atoms]) + '''
loop_
_geom_bond_atom_site_label_1
_geom_bond_atom_site_label_2
_geom_bond_distance
_geom_bond_site_symmetry_2
_ccdc_geom_bond_type
''' + '\n'.join([x.cif(atoms) for x in bonds]) + '\n'
    with open(cif_path, 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == "__main__":
    print(mol2cif('output_5.mol'))