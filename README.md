

# database

此project用于：
1. 将现有多源数据库导入mysql
2. 使用sqlalchemy提供ORM接口，方便增删改查
3. 打包成pypi包，方便进行安装下载

现有数据库有：

- CSD
- QMOF
- CoRE

sqlalchemy教程：https://www.liaoxuefeng.com/wiki/1016959663602400/1017803857459008

mysql的连接：`engine = create_engine('mysql+mysqlconnector://root:digitalmofs@actvis.cn:9049/mofsdb')`


## 结构操作总结

### core和qmof的cif差异

CoRE和QMOF数据集都有MOF对应的cif文件，但是即使是相同的MOF，文件的也存在不同，如下图所示（以`ABAVIJ`为例）

- 属性上：两者存在以下一一对应关系，关键的属性两者都能对上。—— 因为cif 属性之间是无序的。本质上是一个键值对，类似字典。
- 数值上：具体的数字不太相同，甚至有比较大的差异，可以看到其中`_cell_angle_beta`差异非常明显。——出现这个问题是因为零点的取法不一样。

![image-20210716164808158](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205101739866.png)

### xyz转cif 初步分析

![image-20220510174208318](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205101742814.png)

ASE库：https://wiki.fysik.dtu.dk/ase/


### json cif xyz 的关系

输入输出都以ase.atoms为基准。

可使用adaptor`AseAtomsAdaptor().get_atoms()` 将上一步读取的pymatgen的structure类 转换为ase的atoms类。

![image-20220330152233732](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205101739075.png)

ase.atoms可转化为mofs的三种格式。xyz，json只包含了空间结构信息，cif文件还包含了pbe结果的key（没有值），对称信息，化学式。

![image-20220510174231515](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205101742382.png)



### mol 转化为 cif

CSD python API文档：https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_doc_index.html

我们在API中搜索mol，发现原子结构可输出为‘mol2’, ‘sdf’, ‘mol’ or ‘cif’这四种

![image-20220510171915285](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205101719973.png)

因此可通过CSD API转换，样例如下：

```python
from ase.io import read, write
import ccdc


# cif = read('example/ABEFUL.cif')

entry = ccdc.entry.Entry()
entry.from_string('example/ABEFUL.cif', format='cif')


with open('example/ABEFUL.mol', "w") as f:
    f.write(entry.to_string("mol"))
```



