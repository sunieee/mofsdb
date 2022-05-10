# 获取MOFs配体信息

此仓库用于：获取MOFs配体信息，通过以下两个步骤进行：

[TOC]

## 1. 在文本中挖掘CAS号

![image-20220509144942760](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205091449517.png)

从这个pdf文档（http://actvis.cn/data2/share/file ）中提取所有种类的CAS号，我已经转换为txt了（通过https://gitee.com/sun__ye/mofs-paper/tree/master/p2t ），可以使用正则匹配的方法取得CAS号

![image-20220509145447332](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205091454925.png)

通过匹配正则表达式为`\d+-\d+-\d+`的pattern得到以下结果，后面加起来数量为1795多于1760,说明可能有重复。

```
all: 1760
一元羧基类—MOFs材料单体: 156
二元羧基类—MOFs材料单体: 71
四元羧基类—MOFs材料单体: 97
多元羧基类—MOFs材料单体: 31
羧酸含氮混合类—MOFs材料单体: 134
咪唑类—MOFs材料单体: 40
吡啶类—MOFs材料单体: 158
三氮唑类—MOFs材料单体: 18
四氮唑类—MOFs材料单体: 27
其他含杂氮类—MOFs材料单体: 50
卤素类—MOFs材料单体: 199
羟基类—MOFs材料单体: 56
磷酸类—MOFs材料单体: 21
磺酸类—MOFs材料单体: 14
离子类—MOFs材料单体: 64
其它类—MOFs材料单体: 659
```

## 2. 通过CAS号检索详细信息

从PubChem（https://pubchem.ncbi.nlm.nih.gov/ ）搜索这些CAS，通过API（https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest ）查询到这些CAS对应的基本信息，也可以直接写爬虫脚本在主页上模拟搜索。将这些信息记录在表格csv或json中（包括总结信息，越详细越好，如果是csv放在同一文件，如果是json，放在同一文件夹，最后转换为csv文件），比如CAS为`94084-75-0`的单体：

```
Compound CID: 10330479  
MF: C11H10N2O2  MW: 202.21g/mol  
IUPAC Name: 4-(imidazol-1-ylmethyl)benzoic acid  
Isomeric SMILES: C1=CC(=CC=C1CN2C=CN=C2)C(=O)O  
InChIKey: PBTHRDAMTTXZFL-UHFFFAOYSA-N  
InChI: InChI=1S/C11H10N2O2/c14-11(15)10-3-1-9(2-4-10)7-13-6-5-12-8-13/h1-6,8H,7H2,(H,14,15)  
Create Date: 2006-10-25
```
或
```json
[
   	{
		"cid": "10330479",
		"cmpdname": "4-(1H-imidazol-1-ylmethyl)benzoic acid",
		"cmpdsynonym": ["4-(1H-imidazol-1-ylmethyl)benzoic acid","94084-75-0","4-(imidazol-1-ylmethyl)benzoic Acid","4-((1H-Imidazol-1-yl)methyl)benzoic acid","4-[(1H-imidazol-1-yl)methyl]benzoic acid","CHEMBL160003","SCHEMBL4492287","YSCK0036","OKY-070","BBL031427","MFCD09736739","STL259912","ZINC12370278","AKOS000142557","MCULE-8701842154","AM806006","DA-23000","VS-10490","4-(1h-imidazole-1-ylmethyl) benzoic acid","Benzoic acid, 4-(1H-imidazol-1-ylmethyl)-","CS-0035980","FT-0757942","EN300-37084","F2158-0085"],
		"mw": "202.210",
		"mf": "C11H10N2O2",
		"polararea": "55.100",
		"complexity": "225.000",
		"xlogp": "1.100",
		"heavycnt": "15",
		"hbonddonor": "1",
		"hbondacc": "3",
		"rotbonds": "3",
		"inchi": "InChI=1S/C11H10N2O2/c14-11(15)10-3-1-9(2-4-10)7-13-6-5-12-8-13/h1-6,8H,7H2,(H,14,15)",
		"isosmiles": "C1=CC(=CC=C1CN2C=CN=C2)C(=O)O",
		"inchikey": "PBTHRDAMTTXZFL-UHFFFAOYSA-N",
		"iupacname": "4-(imidazol-1-ylmethyl)benzoic acid",
		"annothits": ["Biological Test Results","Classification","Literature","Names and Identifiers","Patents","Safety and Hazards"],
		"annothitcnt": "6",
		"aids": [7810,7815,7816,7820,18991,1159607,1272365],
		"cidcdate": "20061025",
		"sidsrcname": ["001Chemical","A&J Pharmtech CO., LTD.","A2B Chem","AA BLOCKS","AbaChemScene","abcr GmbH","ABI Chem","Achemica","Activate Scientific","AK Scientific, Inc. (AKSCI)","AKos Consulting & Solutions","Alichem","Ambeed","Ambinter","Angel Pharmatech Ltd.","Apexmol","AstaTech, Inc.","Aurora Fine Chemicals LLC","Aurum Pharmatech LLC","BenchChem","Biosynth Carbosynth","BLD Pharm","BOC Sciences","Chem-Space.com Database","Chembase.cn","ChEMBL","Chemenu Inc.","Chemhere","Chemieliva Pharmaceutical Co., Ltd","ChemMol","ChemSpider","ChemTik","Clearsynth","Combi-Blocks","Day Biochem","Debye Scientific Co., Ltd","DiscoveryGate","Enamine","eNovation Chemicals","EPA DSSTox","ET Co.,Ltd.","Finetech Industry Limited","Founder Pharma","Google Patents","IBM","Innovapharm","Japan Chemical Substance Dictionary (Nikkaji)","Key Organics/BIONET","LabNetwork, a WuXi AppTec Company","Life Chemicals","Matrix Scientific","Mcule","MolCore BioPharmatech","Molepedia","MolPort","MuseChem","NextBio","NextMove Software","Norris Pharm","PATENTSCOPE (WIPO)","Pi Chemicals","SCRIPDB","Smolecule","Springer Nature","SureChEMBL","SynHet - Synthetic Heterocycles","Syntree","THE BioTek","Thomson Pharma","TimTec","UW Madison, Small Molecule Screening Facility","Vitas-M Laboratory","Wutech","ZINC"],
		"depcatg": ["Chemical Vendors","Curation Efforts","Governmental Organizations","Journal Publishers","Legacy Depositors","Research and Development","Subscription Services"]
	}
]
```

![image-20220509143318370](https://gitee.com/sun__ye/gallery/raw/master/g1121/202205091449816.png)

调用API样例：https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/94084-75-0/synonyms/XML

对于任何属性都能很快得到，目前的问题是，我们需要哪些属性？



