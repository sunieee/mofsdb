

# %%
with open("/mnt/data1/csd/CCDC/CSD_2022/csd/subsets/CSD_MOF_subsets/Non-disordered_MOF_subset.gcd", 'r') as f:
    MOFS = f.readlines()

len(MOFS)

# %%
from codecs import ignore_errors
import os
dirname = "/mnt/data1/csd/json/simple"
files = os.listdir(dirname)
print(len(files))

# %%
import json
with open(os.path.join(dirname, files[0])) as f:
    dic = json.load(f)
print(dic)


# %%
import pandas as pd
from pandas import DataFrame


# data_path = 'data.csv'
data_path = '/mnt/data1/csd/data.csv'
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = DataFrame(columns=dic.keys())

print(df)

# %% 将files重新设定为没有传入的行

if os.path.exists('invalid.txt'):
    with open("invalid.txt", 'r') as f:
        files = f.read().split("\n")
print(files)

# %%

def delete(f):
    if os.path.exists(f):
        os.remove(f)

for x in files:
    delete(os.path.join("/mnt/data1/csd/json/simple", x))
    delete(os.path.join("/mnt/data1/csd/json/all", x))


# %% 删除具有重复索引的行
df.set_index('identifier', inplace=True)
df = df[~df.index.duplicated(keep='first')]
df.describe()

# %% 删除未命名列

def dropun(X):
    for x in X.columns:
        if x[:7]=='Unnamed':
            X=X.drop(columns=[x])
    return X
df = dropun(df)

# %% 在保存前需要重设索引
df.reset_index(inplace=True)
df.describe()

# %%
invalid = []
files.sort()
for x in files:
    filename = os.path.join(dirname, x)
    with open(filename) as f:
        try:
            dic = json.load(f)
        except Exception as e:
            print(x)
            invalid.append(x)            
    df = df.append(dic, ignore_index=True)

print(invalid)
print(df)

# %% 将输出结果保存
with open("invalid.txt", 'w') as f:
    f.write('\n'.join(invalid))
# %%
df.to_csv(data_path, encoding='utf_8_sig')

# %% 
des = df.describe(include="all")
des.loc['valid_ratio'] = des.loc['count'] / len(df)
des.loc['true_count'] = df[df==True].count()
des.loc['true_ratio'] = des.loc['true_count'] / des.loc['count']
des.loc['dtypes'] = df.dtypes

des = des.T
des

#%%
des.drop(columns=['mean', 'std','min','25%','50%','75%','max'], inplace=True)

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)
des.to_csv("describe.csv", encoding='utf_8_sig')


# %%
import collections
col_length = collections.defaultdict(int)
for col in df.columns:
    if df.dtypes[col] == 'object':
        print(col)
        for i in range(len(df)):
            v = str(df.loc[i, col])
            col_length[col] = max(col_length[col], len(v))
print(col_length)

# %%
def get_min_length(l):
    if l <= 15:
        return 15
    k = 16
    while l >= k:
        k *= 2
    return k-1

col_min_length = {}
for k, v in col_length.items():
    col_min_length[k] = get_min_length(v)
print(col_min_length)

# %%
# varchar一般适用于英文和数字，Nvarchar适用中文和其他字符，其中N表示Unicode常量，可以解决多语言字符集之间的转换问题
from sqlalchemy.types import VARCHAR, Float, Integer, Boolean, Text
dtypedict = {
  'str': VARCHAR(length=255),
  'int': Integer(),
  'float': Float()
}

# 关于VARCHAR与TEXT: https://blog.csdn.net/brycegao321/article/details/78038272
type_dic = {}
for k, v in df.dtypes.items():
    if v == 'bool':
        type_dic[k] = Boolean()
    elif v == 'float64':
        type_dic[k] = Float()
    elif col_min_length.get(k, 255) > 1024:
        type_dic[k] = Text()
    else:
        type_dic[k] = VARCHAR(length=col_min_length.get(k, 255))

# %%
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:digitalmofs@actvis.cn:9049/mofsdb')
con = engine.connect()

# CREATE DATABASE `mofsdb` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
# https://blog.csdn.net/stone0823/article/details/89447982
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
df.to_sql(name='csd', con=con, if_exists='replace', index=False, 
        dtype=type_dic, chunksize=1000)

con.execute('ALTER TABLE csd ADD PRIMARY KEY (`identifier`);')


# %%
