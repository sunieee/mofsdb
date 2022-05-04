from pymatgen.core import Molecule
from pymatgen.core.bonds import CovalentBond
from pymatgen.io.cif import CifParser


if __name__ == '__main__':
    # 读取cif 文件
    parser = CifParser('MOF.cif')
    structure = parser.get_structures()[0]
    # cif文件转mol，以便使用相关接口（能否省略，直接读取成为mol）
    mol = Molecule.from_sites(structure.sites)
    bonds = []  # useless
    # 遍历site,判断是否成键
    n = len(mol.sites)
    # 建立连接图
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        site1 = mol.sites[i]
        for j in range(i + 1, n):
            try:
                site2 = mol.sites[j]
                if CovalentBond.is_bonded(site1, site2):
                    bonds.append(CovalentBond(site1, site2))
                    g[i][j] = 1
                    g[j][i] = 1
            except ValueError:
                pass
    print(bonds)

    def need_break(node: int) -> (bool, int):
        c_num, o_num, idx = 0, 0, -1
        for i in range(n):
            if g[node][i]:
                site = mol.sites[i]
                if site.species_string == 'C':
                    c_num += 1
                    idx = i
                if site.species_string == 'O':
                    o_num += 1
        return c_num == 1 and o_num == 2, idx

    # 遍历原子，查找需要去除的bond
    break_bonds = set()

    for i in range(n):
        flag, j = need_break(i)
        if flag:
            break_bonds.add((i, j))
            mol, break_part = mol.break_bond(i, j)
    # 存储为cif文件
    mol.to('file.cif')
    print(mol)





