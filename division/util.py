import os
from pymatgen.core import Structure
from pymatgen.analysis import structure_matcher
import numpy as np
from ase.io import read
from pymatgen.analysis.graphs import StructureGraph
from pymatgen.analysis import local_env
from ase import neighborlist
import warnings
import shutil


def rm_r(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def deduplicate(folder, new_folder):
    mofs = [] #initialize list to store Pymatgen structures
    entries = os.listdir(folder) #get all CIFs
    entries.sort() #alphabetical sort

    #for every CIF, store Pymatgen Structure in list
    for entry in entries:

        if '.cif' not in entry:
            continue
        
        #read CIF
        mof_temp = Structure.from_file(os.path.join(folder,entry),primitive=False)

        #tag Pymatgen structure with its name
        mof_temp.name = entry
        mofs.append(mof_temp)

    #Initialize StructureMatcher
    sm = structure_matcher.StructureMatcher(primitive_cell=True)

    #Group structures
    groups = sm.group_structures(mofs)
    #Write out set of only unique CIFs
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    for group in groups:
        mof_temp = group[0]
        mof_temp.to(filename=os.path.join(new_folder,mof_temp.name))

    return str(len(groups))+' unique out of '+str(len(entries))+' total'


def dist_check_generate_bonds(pre_path):
    mof = read(pre_path)
    cutoff = 0.75  # interatomic distance threshold
    d = mof.get_all_distances()
    upper_diag = d[np.triu_indices_from(d, k=1)]
    # print(d)
    for entry in upper_diag:
        if entry < cutoff:
            return False # 'Interatomic distance issue'
    
    bonds_info = '''loop_
_geom_bond_atom_site_label_1
_geom_bond_atom_site_label_2
_geom_bond_distance
'''

    with open(pre_path, 'r') as f:
        content = f.read()

    atom_lis = []
    content = content.split('loop_\n')[2]
    index = 1
    for ix, line in enumerate(content.split('\n')):
        line = line.strip()
        if line == '_atom_site_label':
            index = ix
        if len(line.split()) > 1:
            atom_lis.append(line.split()[index])
    # print(atom_lis)

    l = d.shape[0]
    for i in range(l):
        for j in range(i+1, l):
            if d[i][j] < 2:
                bonds_info += f"{atom_lis[i]}\t{atom_lis[j]}\t{d[i][j]}\n"
    with open(pre_path, 'a') as f:
        f.write(bonds_info)
    return True


def lone_atom_check(path):
    mof = Structure.from_file(path)
    nn = local_env.CrystalNN()
    graph = StructureGraph.with_local_env_strategy(mof, nn)
    for j in range(len(mof)):
        nbr = graph.get_connected_sites(j)
        if not nbr:
            return False # 'Lone atom issue'
    return True


def false_terminal_oxo_check(path):
    metals = ['Li','Na','K','Rb','Cs','Fr',
    'Be','Mg','Ca','Sr','Ba','Ra',
    'Sc','Y','La','Ac',
    'Ti','Zr','Hf',
    'Mn',
    'Fe',
    'Co',
    'Ni',
    'Cu','Ag',
    'Zn','Cd',
    'Al','Ga','In','Tl']

    # Read in CIF, ignoring ASE warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        structure = read(path)

    # Get list of atomic symbols
    syms = np.array(structure.get_chemical_symbols())

    # Is one of the specified metals in this MOF
    if not any(item in syms for item in metals):
        return True

    # Initialize neighbor list
    cutoff = neighborlist.natural_cutoffs(structure)
    nl = neighborlist.NeighborList(cutoff,self_interaction=False,bothways=True)
    nl.update(structure)

    # For every site, check if it is a terminal metal-oxo
    for i, sym in enumerate(syms):
        # Confirm site is in pre-specified metal list
        if sym not in metals:
            continue

        # Get neighbors to metal
        bonded_atom_indices = nl.get_neighbors(i)[0]
        if bonded_atom_indices is None:
            continue
        bonded_atom_symbols = syms[bonded_atom_indices]

        # For every neighbor, check if it's a terminal oxo
        for j, bonded_atom_symbol in enumerate(bonded_atom_symbols):

            # Confirm neighbor is an O atom
            if bonded_atom_symbol != 'O':
                continue

            # Check if the O atom is only bound to the metal
            cn = len(nl.get_neighbors(bonded_atom_indices[j])[0])
            if cn == 1:
                return False # 'Missing H on terminal oxo'
    return True