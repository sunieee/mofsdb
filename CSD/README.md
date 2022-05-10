# CSD

[CSD数据库调研点击此处](http://blog.actvis.cn/blog/post/admin/CSD%E6%95%B0%E6%8D%AE%E5%BA%93%E5%AD%97%E6%AE%B5-%E5%85%A5%E5%BA%93)，CSD官网中文API、CSD下载须知见其他两个markdown

## CSD数据库信息

包含以下两类信息：

### 结构

- 为纯字符串，文件格式：cif, xyz
- 单个大小 5～10kb
- 可以被ase库读取解析、标准化，并且ase支持读文件，但不支持直接从数据库导入（ASE库：https://wiki.fysik.dtu.dk/ase/）

用于从CSD API中提取结构文件，这里提取的是`Non-disordered_MOF_subset.gcd`中的MOF（MOF的有序子集，共84898个，具体见[CSD数据库调研](http://blog.actvis.cn/blog/post/admin/CSD%E6%95%B0%E6%8D%AE%E5%BA%93%E5%AD%97%E6%AE%B5-%E5%85%A5%E5%BA%93)）

输出到`/mnt/data1/csd/cif/all`目录下，获取代码见`get_cif()`

下载链接：http://actvis.cn/data1/csd/cif

![image-20220505182405725](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205051824326.png)

这些cif文件以`<mof-id>.cif`命名，这些MOF的CSD参数数据见CSD子仓库


### 可读取属性

可读取属性文件：
- 样例见all.json, simple.json
- 可读取属性json文件：/mnt/data1/csd/json/ 路径下，以identifiers命名
- 可读取属性表格：/mnt/data1/csd/data.csv
- 初步数据处理结果：describe.csv (网页版： [describe.html](http://actvis.ml:9043/sy/Desktop/database/CSD/describe.html))
- 字段分析表格：https://shimo.im/sheets/NJkbEv9gznTJjyqR/kP7E7

属性分类：
1. 条目(entry)属性，如：identifier ABEBUF。
2. 晶体(crystal)属性（描述符）：如z_prime，cell_volume 晶胞体积, smiles
3. 分子(molecule)属性，如：molecular_weight 分子量，components 组成成分

注意：raw属性有很多，但是过滤掉一些没用的属性（unique=1, count=0, len>1w）之后剩下的熟悉已经不多，共57个，分别为：
1. entry: 34个
2. crystal: 13个
3. molecule: 10个

## 入库过程

首先使用`get_dic.py`中定义的函数将数据库导出为json
- `get_dic(True)`：导出简化版的json，放在`/mnt/data1/csd/json/simple/`目录下
- `get_dic()`：导出所有可读取字段的json，放在`/mnt/data1/csd/json/all/`目录下
- `generate_example(identifier)`: 生成样例，all.json与simple.json分别对应两个样例

其次使用`upload.py`
- 读入json，并创建dataframe表格
- 将dataframe表格导入数据库，运行过程出错，详见[upload.html](http://actvis.ml:9043/sy/Desktop/database/CSD/upload.html)


