# fommater

提供各种格式转为cif的方式

```
conda install -c conda-forge rdkit

```


## mol转cif需求

![image-20220512163805286](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121638902.png)

### 需求1：#line1 ‘data_output_5_0511’即data_文件名或代码中的cif_name参数

​	    # line2 时间为当日

​	    #图中后续不变

<img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121511228.png" alt="image-20220512150825548" style="zoom:67%;" />

### 需求2：#圈内值‘10.0000’改为代码内rate参数（忘记设置成全局量了，目前为40）

​	    #图中后续不变

<img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121511100.png" alt="img" style="zoom:67%;" /><img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121511806.png" alt="img" style="zoom:67%;" />

### 需求3：#该模块改为代码中对应模块

<img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121511626.png" alt="img" style="zoom: 67%;" /><img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121511368.png" alt="img" style="zoom:67%;" />



### 需求4：#该模块改为代码中对应模块

<img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121512848.png" alt="img" style="zoom:67%;" /><img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121512101.png" alt="img" style="zoom:67%;" />

\#其余

<img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121512602.png" alt="img" style="zoom:67%;" /><img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121512695.png" alt="img" style="zoom:67%;" /> 

### 需求5（待定）：对方向族（例子：苯环）的成键进行更改，由三个D三个S改为六个A

<img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121512543.png" alt="img" style="zoom: 33%;" /><img src="https://gitee.com/sun__ye/gallery/raw/master/g1121/202205121512648.png" alt="img" style="zoom:67%;" />

注释：即六个原子首尾相连且键由三个D三个S组成，则将键换位六个A
