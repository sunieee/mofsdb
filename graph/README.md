# Graph

探究如何讲cif转换为图结构以进行下游任务：

## 转换为图结构：QMOF方案

我们使用最为通用的cif格式来保存结构信息，运行时再生成图。生成图的过程使用了QMOF处理图的流程，见`data.py/CIFData`（依赖：torch, pymatgen, ase）

该方法利用pymatgen,ASE 库解析cif文件得到mofs的原子结构（包括邻居和空间信息）。基于该结构，用距离阈值定义化学键，最后使用n最近邻建图。

QMOF代码在：https://github.com/arosen93/QMOF/blob/main/machine_learning/cgcnn/cgcnn/data.py#L327

### 输出

- 2个邻接表，表示单个mofs原子间的连接关系。（邻居id存一个表，属性另一个表；取最近邻的操作保证表格列数相同）
- 每个节点的特征向量。
- 整张图的标签和id。

### 输入

数据文件夹root_dir包含一系列cif文件

CIF的语法较复杂，完整cif文件包含的内容很多。其中各项含义可见[CIF文件详解 - 百度文库 (baidu.com)](https://wenku.baidu.com/view/7d6aae12580216fc710afd11.html)， 官方文档[(IUCr) A guide to CIF for authors](https://www.iucr.org/resources/cif/documentation/cifguide)。

```
data_image0
_cell_length_a 16.991
_cell_length_b 16.991
_cell_length_c 16.991
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_symmetry_space_group_name_H-M "P 1"
_symmetry_int_tables_number 1
loop_
_symmetry_equiv_pos_as_xyz
'x, y, z'
loop_
_atom_site_label
_atom_site_occupancy
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_thermal_displace_type
_atom_site_B_iso_or_equiv
_atom_site_type_symbol
C1 1.0000 0.37705 0.00790 0.62295 Biso 1.000 C
C2 1.0000 0.36851 0.89914 0.68750 Biso 1.000 C
H1 1.0000 0.37770 0.85890 0.72340 Biso 1.000 H
C3 1.0000 0.40610 0.08550 0.59390 Biso 1.000 C
N1 1.0000 0.40973 0.96832 0.68278 Biso 1.000 N
```

### 建图算法流程

1. 通过ase反对称性解析标准化cif
2. 再通过Structure.from_file(id0.cif）将cif读入，转化为pymatgen.structure类
3. 取radius距离8以内的原子（一般来说，这个阈值为2以内才会成键），得到原子的所有邻居all_nbrs: Structure.get_all_neighbors
4. 建图 ，得到nbr_id，nbr_fea： 以radius为阈值建边，取最近的max_num_nbr个。不足的对属性向量进行进行正规化（？）.最后调用GaussianDistance.expand

总结：根据距离阈值连化学键，再取最邻近的n个，（nbr_fea也可以看出是键的特征）属性中有一些人工提取的距离特征（正规化，高斯距离）。

改进：额外考虑键的3维特征（ALIGNN），额外考虑子图特征（官能团、次级结构）。

### 样例

ABEFUL.cif中共184个原子，输出为：

```
torch.Size([184, 12, 41]) tensor([[[0.0000e+00, 0.0000e+00, 1.0131e-42,  ..., 0.0000e+00,
          0.0000e+00, 0.0000e+00],
         [0.0000e+00, 0.0000e+00, 1.0131e-42,  ..., 0.0000e+00,
          0.0000e+00, 0.0000e+00],
         [0.0000e+00, 0.0000e+00, 1.0131e-42,  ..., 0.0000e+00,
          0.0000e+00, 0.0000e+00],
         ...,
         [0.0000e+00, 0.0000e+00, 0.0000e+00,  ..., 0.0000e+00,
          0.0000e+00, 0.0000e+00],
         [0.0000e+00, 0.0000e+00, 0.0000e+00,  ..., 0.0000e+00,
          0.0000e+00, 0.0000e+00],
         [0.0000e+00, 0.0000e+00, 0.0000e+00,  ..., 0.0000e+00,
          0.0000e+00, 0.0000e+00]]])
torch.Size([184, 12]) tensor([[157, 158, 155,  ..., 138, 142, 139],
        [164, 167, 163,  ..., 142, 138, 144],
        [ 58,  74,  50,  ..., 142,  67,  90],
        ...,
        [183, 178, 153,  ..., 112, 136, 134],
        [180, 179, 147,  ..., 106, 130, 133],
        [181, 179, 151,  ..., 112, 136, 134]])
```

第一个是nbr_fea邻居特征，共41维，第二个是nbr_fea_idx，每个原子与最近的12个原子相连接（这里并没有科学依据，可能因为QMOF里的GNN算法简化了图结构）