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



![image-20210716164808158](https://img2022.cnblogs.com/blog/1339851/202204/1339851-20220406125837965-1544832231.png)

### xyz转cif 初步分析

![image-20210716162637892](https://img2022.cnblogs.com/blog/1339851/202204/1339851-20220406125839100-780638557.png)

ASE库：https://wiki.fysik.dtu.dk/ase/

CSD python API文档：https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_doc_index.html


### json cif xyz 的关系

输入输出都以ase.atoms为基准。

可使用adaptor`AseAtomsAdaptor().get_atoms()` 将上一步读取的pymatgen的structure类 转换为ase的atoms类。

![image-20220330152233732](https://img2022.cnblogs.com/blog/1339851/202204/1339851-20220406125827013-137475341.png)

ase.atoms可转化为mofs的三种格式。xyz，json只包含了空间结构信息，cif文件还包含了pbe结果的key（没有值），对称信息，化学式。

![image-20220330152433068](https://img2022.cnblogs.com/blog/1339851/202204/1339851-20220406125834907-1550414170.png)





