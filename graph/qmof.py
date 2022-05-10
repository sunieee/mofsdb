import csv
import json
import os
import random
import warnings
import pickle
from ase.io import read, write

import numpy as np
import torch
from pymatgen.core.structure import Structure
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataloader import default_collate
from torch.utils.data.sampler import SubsetRandomSampler


class GaussianDistance(object):
    """
    Expands the distance by Gaussian basis.

    Unit: angstrom
    """

    def __init__(self, dmin, dmax, step, var=None):
        """
        Parameters
        ----------

        dmin: float
          Minimum interatomic distance
        dmax: float
          Maximum interatomic distance
        step: float
          Step size for the Gaussian filter
        """
        assert dmin < dmax
        assert dmax - dmin > step
        self.filter = np.arange(dmin, dmax+step, step)
        if var is None:
            var = step
        self.var = var

    def expand(self, distances):
        """
        Apply Gaussian distance filter to a numpy distance array

        Parameters
        ----------

        distance: np.array shape n-d array
          A distance matrix of any shape

        Returns
        -------
        expanded_distance: shape (n+1)-d array
          Expanded distance matrix with the last dimension of length
          len(self.filter)
        """
        return np.exp(-(distances[..., np.newaxis] - self.filter)**2 /
                      self.var**2)


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


class CIFData(Dataset):
    """
    The CIFData dataset is a wrapper for a dataset where the crystal structures
    are stored in the form of CIF files. The dataset should have the following
    directory structure:

    root_dir
    ├── id_prop.csv
    ├── atom_init.json
    ├── id0.cif
    ├── id1.cif
    ├── ...

    id_prop.csv: a CSV file with two columns. The first column recodes a
    unique ID for each crystal, and the second column recodes the value of
    target property.

    atom_init.json: a JSON file that stores the initialization vector for each
    element.

    ID.cif: a CIF file that recodes the crystal structure, where ID is the
    unique ID for the crystal.

    Parameters
    ----------

    root_dir: str
        The path to the root directory of the dataset
    max_num_nbr: int
        The maximum number of neighbors while constructing the crystal graph
    radius: float
        The cutoff radius for searching neighbors
    dmin: float
        The minimum distance for constructing GaussianDistance
    step: float
        The step size for constructing GaussianDistance
    disable_save_torch: bool
        Don't save torch files containing CIFData crystal graphs
    random_seed: int
        Random seed for shuffling the dataset

    Returns
    -------

    atom_fea: torch.Tensor shape (n_i, atom_fea_len)
    nbr_fea: torch.Tensor shape (n_i, M, nbr_fea_len)
    nbr_fea_idx: torch.LongTensor shape (n_i, M)
    target: torch.Tensor shape (1, )
    cif_id: str or int
    """

    def __init__(self, root_dir, max_num_nbr=12, radius=8, dmin=0, step=0.2):
        self.root_dir = root_dir
        self.max_num_nbr, self.radius = max_num_nbr, radius
        assert os.path.exists(root_dir), 'root_dir does not exist!'
        self.gdf = GaussianDistance(dmin=dmin, dmax=self.radius, step=step)

    def __len__(self):
        return len(os.listdir(self.root_dir))

    def __getitem__(self, cif_id):
        cif_id = cif_id.replace('ï»¿', '')

        # 反对称性解析标准化cif
        path = os.path.join(self.root_dir, cif_id+'.cif')
        pre_path = os.path.join(self.root_dir, cif_id+'_pre.cif')
        try:
            mof = read(path)
            write(pre_path, mof)
        except:
            return 'Reading cif file failed'
        
        # 成键，得到邻居编号
        crystal = Structure.from_file(pre_path)
        all_nbrs = crystal.get_all_neighbors(
            self.radius, include_index=True)
        all_nbrs = [sorted(nbrs, key=lambda x: x[1]) for nbrs in all_nbrs]
        
        # 计算邻居特征（这里取最近的12个邻居）
        nbr_fea_idx, nbr_fea = [], []
        for nbr in all_nbrs:
            if len(nbr) < self.max_num_nbr:
                warnings.warn('{} not find enough neighbors to build graph. '
                                'If it happens frequently, consider increase '
                                'radius.'.format(cif_id))
                nbr_fea_idx.append(list(map(lambda x: x[2], nbr)) +
                                    [0] * (self.max_num_nbr - len(nbr)))
                nbr_fea.append(list(map(lambda x: x[1], nbr)) +
                                [self.radius + 1.] * (self.max_num_nbr -
                                                        len(nbr)))
            else:
                nbr_fea_idx.append(list(map(lambda x: x[2],
                                            nbr[:self.max_num_nbr])))
                nbr_fea.append(list(map(lambda x: x[1],
                                        nbr[:self.max_num_nbr])))
        nbr_fea_idx, nbr_fea = np.array(nbr_fea_idx), np.array(nbr_fea)
        nbr_fea = self.gdf.expand(nbr_fea)
        nbr_fea = torch.Tensor(nbr_fea)
        nbr_fea_idx = torch.LongTensor(nbr_fea_idx)

        return nbr_fea, nbr_fea_idx


if __name__ == "__main__":
    data = CIFData('example')
    nbr_fea, nbr_fea_idx = data['ABEFUL']
    print(nbr_fea.shape, nbr_fea)
    print(nbr_fea_idx.shape, nbr_fea_idx)