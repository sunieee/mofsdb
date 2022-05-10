import re
from collections import defaultdict
import json
import os
import pandas as pd


# 第1个清单: 研伸科技
if os.path.exists('data.json'):
    dic = json.load(open("data.json", 'r'))
else:
    with open('研伸科技-mofs配体目录.txt', 'r') as f:
        s = f.read()

    mofs = re.findall(r'\d+-\d+-\d+', s)
    t = ""

    lines = s.split('\n')
    i = 0
    dic = defaultdict(set)
    dic['1'] = set(mofs)
    while i < len(lines):
        line = lines[i]
        if line.startswith('---------------page'):
            i += 1
            line = lines[i]
            if line.split()[0].count('MOFs材料单体'):
                t = "1-" + line.split()[0]
        
        dic[t] |= set(re.findall(r'\d+-\d+-\d+', line))
        i += 1
    
    del dic['']
    # print(dic)
    

# 第2个清单: chemsoon
if '2' not in dic:
    df = pd.read_csv('list.csv', header=None)
    dic['2'] = set(df[3])


dic['all'] = set()
i = 1
while str(i) in dic:
    dic['all'] |= set(dic[str(i)])
    i += 1

print('\n'.join([f"{k}: {len(v)}" for k, v in dic.items()]))

with open('data.json', 'w') as f:
    json.dump({k: list(v) for k, v in dic.items()}, f)