# division

此仓库用于将完整MOF结构分割为次级结构单元 + 配体。分割规则及描述详见`结构分割规则.md`

liruiming 和 mengtao 已有两个实现，此仓库整合并扩展这两个实现，使其能用于任何场景下。

## 四个样例

data文件夹下四个样例的图像分别如下：

![image-20220405174527059](https://images.weserv.nl/?url=gitee.com/sun__ye/gallery/raw/master/g1121/202204051745466.png)

| 样例 | MOF                                                          | 次级结构单元                                                 | 配体                                                         |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | <img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051743810.png" alt="image-20220405172433347" style="zoom:;" /> | <img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051743973.png" alt="image-20220405172459556"  /> | <img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051743756.png" alt="image-20220405172542469" style="zoom:;" /> |
| 2    | <img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051743803.png" alt="image-20220405172654009"  /> | ![image-20220405172823207](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051728987.png) | ![](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051728231.png) |
| 3    | ![image-20220405172906183](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051729805.png) | ![image-20220405172917233](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051729669.png) | ![image-20220405172926713](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051729966.png) |
| 4    | ![image-20220405172946573](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051729765.png) | ![image-20220405172955614](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051729483.png) | ![image-20220405173004295](https://gitee.com/sun__ye/gallery/raw/master/g1121/202204051730149.png) |

## 步骤

整个流程分为三步：

1. 预处理：将非标准格式MOF对应的cif（经过反对称解析:“成键操作”与“P1对称性设置”）转为标准格式
2. 分割：按照规则进行分割，输出到一系列文件，分为次级结构单元和有机配体两类
3. 后处理：读入并建立结构唯一的hash值（如smile名称）来去重，最后以标准格式输出

### 如何进行预处理？

1. 先进行反对称变换，将所有原子都独立出来，不含对称性信息
2. 再通过check_dist将距离小于2的两点之间连边。直接进行分割

### 如何进行分割？

手动解析cif，建图，寻找匹配的pattern并进行切割

### 如何进行后处理？

不需要自己探索去重依据，直接使用QMOF deduplicate工具即可自动去重

## 平台模块设计

![image-20220419103013278](https://images.weserv.nl/?url=gitee.com/sun__ye/gallery/raw/master/g1121/202204191030574.png)

分割模块提供以下功能：

- 上传cif文件：点击按钮上传本地cif文件
- 分割：调用分割模块，将上传的cif按照规则划分
- cif结构展示：展示已有cif和分割结果的三维视图（可展示化学式信息）
- 下载全部分割结果或指定cif文件
- (可选)记录已转换结果，提供列表（如下图）

![image-20220419102134824](https://images.weserv.nl/?url=gitee.com/sun__ye/gallery/raw/master/g1121/202204191021757.png)
