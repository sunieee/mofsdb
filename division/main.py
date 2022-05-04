from ase.io import read, write
import os
from cif import Cif
from util import deduplicate, dist_check_generate_bonds, rm_r
from util import false_terminal_oxo_check, lone_atom_check

def division(path, out_folder):
    tmp_folder = 'output/tmp'   # 中间处理cif结果
    pre_path = 'output/tmp.cif' # 预处理后的cif
    os.makedirs(out_folder, exist_ok=True)
    rm_r(tmp_folder)
    os.makedirs(tmp_folder)

    # 1. 预处理
    # 反对称解析
    try:
        mof = read(path)
        write(pre_path, mof)
    except:
        return 'Reading cif file failed'
    # 失败检测
    # if not false_terminal_oxo_check(pre_path):
    #     return 'Missing H on terminal oxo'
    # if not lone_atom_check(pre_path):
    #     return 'Lone atom issue'
    # 成建操作
    if not dist_check_generate_bonds(pre_path):
        return 'Interatomic distance issue'

    # 2. 分割
    c = Cif()
    c.parse_file(pre_path)
    c.generate_cif(tmp_folder)

    # 3. 后处理
    return deduplicate(tmp_folder, out_folder)


if __name__ == "__main__":
    print(division('data/4/MOF.cif', 'output/4'))
