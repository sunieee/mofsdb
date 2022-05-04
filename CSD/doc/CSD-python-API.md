## 1. 从 CSD 访问数据库条目、晶体和分子

CSD Python API 对数据库条目 ( [`ccdc.entry.Entry`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry))、晶体 ( [`ccdc.crystal.Crystal`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/crystal_api.html#ccdc.crystal.Crystal)) 和分子 ( [`ccdc.molecule.Molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule))进行了区分。为了说明差异，让我们访问 ABEBUF 的数据库条目、晶体和分子。

```python
from ccdc import io
csd_reader = io.EntryReader('CSD')
entry_abebuf = csd_reader.entry('ABEBUF')
cryst_abebuf = csd_reader.crystal('ABEBUF')
mol_abebuf = csd_reader.molecule('ABEBUF')
```

### 1.1. 分子

A[`ccdc.molecule.Molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule)包含分子属性，例如分子量 ( [`ccdc.molecule.Molecule.molecular_weight`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule.molecular_weight)) 和描述符，例如分子是否为有机物 ( [`ccdc.molecule.Molecule.is_organic`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule.is_organic))。

```python
round(mol_abebuf.molecular_weight, 3)  # only want 3 significant figures
317.341
mol_abebuf.is_organic
True
```

该分子还包含用于返回“mol2”或“sdf”格式字符串的[`ccdc.molecule.Molecule.smiles`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule.smiles) 表示形式和函数。[`ccdc.molecule.Molecule.to_string()`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule.to_string)

```python
print(mol_abebuf.smiles)
O=C1Nc2ccccc2C(=O)Nc2ccccc12.c1ccncc1
print(mol_abebuf.to_string('mol2'))  
@<TRIPOS>MOLECULE
ABEBUF
...
```

请注意，从 SMILES 字符串中可以明显看出该分子包含两个不连贯的组件：

- `O=C1Nc2ccccc2C(=O)Nc2ccccc12`
- `c1ccncc1`

单个成分也是分子，可以通过列表访问，并且可以通过属性[`ccdc.molecule.Molecule.components`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule.components)访问具有最大分子量的单个分子。[`ccdc.molecule.Molecule.heaviest_component`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule.heaviest_component)

```python
mol_abebuf.components  
[<ccdc.molecule.Molecule object at ...>,
 <ccdc.molecule.Molecule object at ...>]
[round(mol.molecular_weight, 3) for mol in mol_abebuf.components]
[238.241, 79.1]
print(mol_abebuf.heaviest_component.smiles)
O=C1Nc2ccccc2C(=O)Nc2ccccc12
```

> 描述[性分子文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/molecule.html)和 [`ccdc.molecule.Molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule)API 文档。

### 1.2. 晶体

晶体包含晶体学描述符，例如 Z' ( [`ccdc.crystal.Crystal.z_prime`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/crystal_api.html#ccdc.crystal.Crystal.z_prime)) 和晶胞体积 ([`ccdc.crystal.Crystal.cell_volume`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/crystal_api.html#ccdc.crystal.Crystal.cell_volume))。

```python
cryst_abebuf.z_prime
1.0
round(cryst_abebuf.cell_volume, 3)  # only want 3 significant figures
3229.582
```

可以从 [`ccdc.crystal.Crystal.molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/crystal_api.html#ccdc.crystal.Crystal.molecule)属性中访问晶体结构中的分子。

```python
cryst_abebuf.molecule 
<ccdc.molecule.Molecule object at ...>
print(cryst_abebuf.molecule.smiles)
O=C1Nc2ccccc2C(=O)Nc2ccccc12.c1ccncc1 
```

> 描述[性水晶文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/crystal.html)和 [`ccdc.crystal.Crystal`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/crystal_api.html#ccdc.crystal.Crystal)API 文档。

### 1.3. 条目

CSD 条目包含有关在编辑过程中添加的晶体结构的附加信息。示例包括化学名称 ( [`ccdc.entry.Entry.chemical_name`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry.chemical_name)) 和出版物详细信息 ( [`ccdc.entry.Entry.publication`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry.publication))。

```python
print(entry_abebuf.chemical_name)
5H,11H-Dibenzo(b,f)(1,5)diazocine-6,12-dione pyridine clathrate
print(entry_abebuf.publication)  
Citation(authors='S.W.Gordon-Wylie, E.Teplin, J.C.Morris,
          M.I.Trombley, S.M.McCarthy, W.M.Cleaver, G.R.Clark',
         journal='Journal(Crystal Growth and Design)',
         volume='4', year=2004, first_page='789',
         doi='10.1021/cg049957u')
```

条目中的晶体和分子可以分别从 [`ccdc.entry.Entry.crystal`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry.crystal)和 [`ccdc.entry.Entry.molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry.molecule)属性访问。

```python
entry_abebuf.crystal 
<ccdc.crystal.Crystal object at ...>
entry_abebuf.crystal.z_prime
1.0
entry_abebuf.molecule 
<ccdc.molecule.Molecule object at ...>
print(entry_abebuf.molecule.smiles)
O=C1Nc2ccccc2C(=O)Nc2ccccc12.c1ccncc1
```

## 2. 读写分子

假设我们想将我们的分子写入一个名为 `abebuf.mol2`.

```python
file_name = 'abebuf.mol2'
```

该[`ccdc.io`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#module-ccdc.io)模块具有三种类型的编写器： [`ccdc.io.EntryWriter`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#ccdc.io.EntryWriter), [`ccdc.io.CrystalWriter`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#ccdc.io.CrystalWriter), [`ccdc.io.MoleculeWriter`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#ccdc.io.MoleculeWriter). 这些都是可以使用 Python`with`语法的上下文管理器。

```python
with io.MoleculeWriter(file_name) as mol_writer:
    mol_writer.write(mol_abebuf)
```

现在我们已经将一个分子写入文件系统，我们可以说明如何从文件中读取一个分子。

```python
mol_reader =  io.MoleculeReader(file_name)
mol = mol_reader[0]  # get the first molecule in the file
print(mol.identifier)
ABEBUF
print(mol.smiles)
O=C1Nc2ccccc2C(=O)Nc2ccccc12.c1ccncc1
len(mol.components)
2
```

> A[`ccdc.io.MoleculeReader`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#ccdc.io.MoleculeReader)是一个**迭代器**，可以包含零个或多个分子。这就是为什么我们必须明确地从中获得第一个分子。

另请注意，包含多个分子的分子文件的概念与**分子可以包含多个不同组件**的概念不同。因此，从分子阅读器中提取的第一个分子具有两个成分。

## 3. 搜索 CSD 

有几种主要的搜索 CSD 的方法：

- 根据条目对应的数据进行文本数字搜索（[`ccdc.search.TextNumericSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.TextNumericSearch)）；
- 化学相似条目的相似性搜索（[`ccdc.search.SimilaritySearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SimilaritySearch)）；
- 子结构搜索，包括具有 3D 几何约束和测量的搜索 ( [`ccdc.search.SubstructureSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch))；
- 减少基于晶体单元参数的单元搜索（[`ccdc.search.ReducedCellSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.ReducedCellSearch)）。

### 3.1. 文本和数字搜索

假设有人对阿司匹林的物理性质感兴趣，因此想找到包含阿司匹林晶体结构并记录熔点的出版物。

这可以使用[`ccdc.search.TextNumericSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.TextNumericSearch).

```python
from ccdc.search import TextNumericSearch
text_numeric_search = TextNumericSearch()
text_numeric_search.add_compound_name('aspirin')
identifiers = [h.identifier for h in text_numeric_search.search()]
```

多年来，通用名称和化学名称的分配有些武断地分配给 CSD 的同义词和复合名称字段。因此，我们还需要搜索同义词字段以使搜索全面。

```python
text_numeric_search.clear()
text_numeric_search.add_synonym('aspirin')
identifiers.extend([h.identifier for h in text_numeric_search.search()])
```

最后，我们遍历标识符。为了确保我们避免重复，我们可以利用 Python 的内置集合功能。对于每个标识符，我们从 CSD 获取相关条目，并检查它是否具有关联的熔点，如果有，我们会写出标识符、DOI 和熔点信息。

```python
for identifier in sorted(set(identifiers)):
    e = csd_reader.entry(identifier)
    if e.melting_point:
        print('%-8s http://dx.doi.org/%-25s %s' % (e.identifier,
                                                   e.publication.doi,
                                                   e.melting_point))

ACMEBZ   http://dx.doi.org/10.1107/S0567740881006729 385K
ACSALA13 http://dx.doi.org/10.1021/ja056455b         135.5deg.C
ACSALA28 http://dx.doi.org/10.1039/D0CC03157G        415 K
BEHWOA   http://dx.doi.org/10.1107/S0567740882005731 401K
CUASPR01 http://dx.doi.org/10.1107/S1600536803026126 above 573 K
HUPPOX   http://dx.doi.org/10.1039/b208574g          91-96 deg.C
HUPPOX01 http://dx.doi.org/None                      91-96 deg.C
NUWTOP01 http://dx.doi.org/10.1039/c2ce06313a        147 deg.C
PIKYUG   http://dx.doi.org/10.1021/acs.cgd.8b00718   502 K
```

> 描述性 [文本数字搜索文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/text_numeric_searching.html)和 API 文档。[`ccdc.search.TextNumericSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.TextNumericSearch)`ccdc.search.TextNumericHit`

### 3.2. 分子相似性搜索

假设有人想找出 **CSD 条目占据了哪些空间群**，这些条目包含与 的最重成分相似的化合物`ABEBUF`。如果尝试使用粉末数据解决新化合物的结构，这类信息可能会很有趣。了解化合物可能占据哪些空间群有助于解释数据。这可以使用[`ccdc.search.SimilaritySearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SimilaritySearch).

```python
from ccdc.search import SimilaritySearch
sim_search = SimilaritySearch(mol_abebuf.heaviest_component)
hits = sim_search.search()
len(hits)
33
for h in hits:
    print('%8s %.3f %s' % (h.identifier, h.similarity, h.crystal.spacegroup_symbol))

  ABEBIT 1.000 P-1
  ABEBOZ 1.000 P-1
  ABEBUF 1.000 Pbca
  ISOHAZ 1.000 P-1
  ISOHED 1.000 P212121
  ISOHIH 1.000 P21/n
  LIGREY 0.981 P21/n
LIGREY01 0.981 P21/c
  DMECDC 0.954 P21
  MEANLD 0.954 P21/a
  EQOTIQ 0.849 P21/n
  UCELIX 0.847 P21/c
  DBZCDC 0.828 P21/a
  WUZPAL 0.809 P21/n
  ADOHIM 0.806 P21/c
  WUZNUD 0.792 P21/c
  WUZPEP 0.790 Pbca
  MANTRN 0.788 P212121
  WUZNOX 0.788 Pbca
  ASITOL 0.775 Pca21
  ASITUR 0.775 P-1
  ASIVAZ 0.775 P-1
  TOVZEJ 0.759 P-1
  MUWSOP 0.754 P21/c
  QAFMET 0.750 P21/n
  LOSKAI 0.741 P21/c
  NUJPUE 0.739 P21/c
  TOKZAW 0.739 P-1
  HIRROR 0.735 P21/c
HIRROR01 0.735 P21/n
  LOSKEM 0.706 P21/n
  ARUGOM 0.706 P-1
  JONWOA 0.705 Pbca
```

> 描述性相似性 [搜索文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/similarity_searching.html)和 API 文档。[`ccdc.search.SimilaritySearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SimilaritySearch)[`ccdc.search.SimilaritySearch.SimilarityHit`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SimilaritySearch.SimilarityHit)

### 3.3. 使用 3D 测量进行子结构搜索

#### 3.3.1. 识别相同的分子

假设我们想知道 CSD 中是否还有其他包含`5H,11H-Dibenzo(b,f)(1,5)diazocine-6,12-dione` （最重的组件`ABEBUF`）的结构。

这可以通过设置 a [`ccdc.search.SubstructureSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch)和 a [`ccdc.search.MoleculeSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.MoleculeSubstructure)来实现。

```python
from ccdc.search import SubstructureSearch, MoleculeSubstructure
mol_substructure = MoleculeSubstructure(mol_abebuf.heaviest_component)
substructure_search = SubstructureSearch()
sub_id = substructure_search.add_substructure(mol_substructure)
hits = substructure_search.search()
hits

[ABEBIT,ABEBOZ,ABEBUF,ISOHAZ,ISOHAZ,ISOHED,ISOHIH,ISOHIH]
```

请注意，某些 CSD 条目被此子结构多次命中。如果我们只想对每个结构进行一次点击，我们可以使用 `max_hits_per_structure`参数。下面的示例还说明了如何从子结构命中中获取匹配原子的索引。

```python
hits = substructure_search.search(max_hits_per_structure=1)
len(hits)
6
for h in hits:
    print('%s: (%s)' % (h.identifier, ', '.join('%d' % i for i in h.match_atoms(indices=True))))  
ABEBIT: (26, 27, 0, ..., 23, 21, 11)
ABEBOZ: (0, 1, 2, ..., 22, 24, 26)
ABEBUF: (0, 1, 2, ..., 25, 26, 27)
ISOHAZ: (0, 1, 4, ..., 22, 24, 26)
ISOHED: (10, 11, 14, ..., 32, 34, 36)
ISOHIH: (10, 11, 14, ..., 32, 34, 36)
```

#### 3.3.2. 无环片段的扭转偏好

假设我们有兴趣找出 2-乙氧基乙氧基片段的扭转偏好。它是否像烷基链一样 180°？

这可以通过设置 a 来实现 [`ccdc.search.SubstructureSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch)，例如从 a 开始 [`ccdc.search.SMARTSSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SMARTSSubstructure)，然后在搜索中添加扭转测量 `ccdc.search.SubstructureSearch.add_torsion_measurement()`。

首先，我们创建一个[`ccdc.search.SMARTSSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SMARTSSubstructure)使用 SMARTS 模式。

```python
from ccdc.search import SMARTSSubstructure
ethoxyethoxy = SMARTSSubstructure('[OD2][CH2]!@[CH2][OD2]')
for qatom in ethoxyethoxy.atoms:  
    print('%d: %s' % (qatom.index, qatom))
...
0: QueryAtom(O)[atom aromaticity: equal to 0, count connected elements equal to 2 from [0: Li 116: Rn ]]
1: QueryAtom(C)[atom aromaticity: equal to 0, hydrogen count, including deuterium: equal to 2]
2: QueryAtom(C)[atom aromaticity: equal to 0, hydrogen count, including deuterium: equal to 2]
3: QueryAtom(O)[atom aromaticity: equal to 0, count connected elements equal to 2 from [0: Li 116: Rn ]]
```

然后我们创建一个[`ccdc.search.SubstructureSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch)并将子结构添加到它。

```python
substructure_search = SubstructureSearch()
sub_id = substructure_search.add_substructure(ethoxyethoxy)
```

[`ccdc.search.QueryAtom`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.QueryAtom)然后，我们可以使用子结构标识符和索引向子结构添加扭转测量。

```python
substructure_search.add_torsion_angle_measurement('TOR1',
    sub_id, 0,
    sub_id, 1,
    sub_id, 2,
    sub_id, 3)
```

为了说明这个搜索，我们将在前五个结构被命中后停止搜索。

```python
hits = substructure_search.search(max_hit_structures=5)
for h in hits:
    print('%8s %7.2f' % (h.identifier,
                        h.measurements['TOR1']))
...
  ABIGEY  176.23
  ABIGEY  162.75
  ABOKAD   64.74
  ABOKAD   58.64
  ABOKAD  -63.53
  ABOKAD   67.31
  ABOKAD   66.00
  ABOKAD   73.18
  ACEJIE   41.31
  ACEJIE  -68.13
  ACEJIE  -64.21
  ACEJIE   67.41
  ACEJIE  -67.65
  ACEJIE   66.83
  ACEJIE  -70.26
  ACEJIE   67.18
  ACIFEZ   70.50
  ACIFEZ   55.07
  ACIFEZ  -70.58
  ACIJOM  180.00
```

#### 3.3.3. 一对官能团的相互作用几何

假设我们有兴趣弄清楚带电吡啶片段与酰胺基团的羰基氧相互作用是否在几何形状上有任何偏好。

这可以通过设置一个 来实现 [`ccdc.search.SubstructureSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch)，例如使用一对 [`ccdc.search.SMARTSSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SMARTSSubstructure)实例，并在感兴趣的原子之间添加一个距离约束 ( [`ccdc.search.SubstructureSearch.add_distance_constraint()`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch.add_distance_constraint))。

然后可以使用[`ccdc.search.SubstructureSearch.add_angle_measurement()`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch.add_angle_measurement) 它来设置两个感兴趣角度的测量值。

![带电吡啶转酰胺联系查询。](https://downloads.ccdc.cam.ac.uk/documentation/API/_images/charged_pyridine_amide_query.png)

子结构搜索以研究带电吡啶基团与酰胺羰基氧相互作用的几何偏好。

```python
charged_pyridine = SMARTSSubstructure('c1ccn(H)cc1')  # indices N:3 H:4
amide = SMARTSSubstructure('C[NH]C(=O)C')  # indices C:2 O:3
substructure_search = SubstructureSearch()
sub1 = substructure_search.add_substructure(charged_pyridine)
sub2 = substructure_search.add_substructure(amide)
```

请注意，我们现在为这个特定的子结构搜索添加了两个不同的子结构。此时，我们可以设置两个子结构中感兴趣的原子之间的距离约束以及角度测量。

```python
substructure_search.add_distance_constraint('D1',
    sub1, 4,
    sub2, 3,
    (0, 2.5),  # distance constraint range
    'Intermolecular')
substructure_search.add_angle_measurement('A1',
    sub1, 3,
    sub1, 4,
    sub2, 3)
substructure_search.add_angle_measurement('A2',
    sub2, 2,
    sub2, 3,
    sub1, 4)
```

为了说明这个搜索，我们将在前五个结构被命中后停止搜索。

```python
hits = substructure_search.search(max_hit_structures=5)
for h in hits:
    print('%s (D1 %.2f) (A1 %.2f) (A2 %.2f)' % (h.identifier, h.constraints['D1'], h.measurements['A1'], h.measurements['A2']))
...
AMEHUX (D1 2.12) (A1 130.21) (A2 124.72)
CUWWEX (D1 1.99) (A1 157.26) (A2 142.09)
DOKPAU (D1 1.93) (A1 133.90) (A2 138.39)
DOKPEY (D1 1.89) (A1 133.08) (A2 138.74)
FEZBUK (D1 2.16) (A1 168.21) (A2 122.84)
```

> 描述[性子结构搜索文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/substructure_searching.html)和[`ccdc.search.SubstructureSearch`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SubstructureSearch), [`ccdc.search.MoleculeSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.MoleculeSubstructure), [`ccdc.search.SMARTSSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.SMARTSSubstructure), [`ccdc.search.ConnserSubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.ConnserSubstructure), [`ccdc.search.QuerySubstructure`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.QuerySubstructure), [`ccdc.search.QueryAtom`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.QueryAtom), [`ccdc.search.QueryBond`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/search_api.html#ccdc.search.QueryBond)API 文档。

## 4. 构象几何分析

CSD 软件提供的功能可以快速验证给定查询分子的完整几何形状。例如，这可用于验证蛋白质-配体结构中配体的结合模式。它还可以为评估构象多晶型物的相对稳定性提供有价值的信息。在本例中，我们将比较 HIV 蛋白酶抑制剂利托那韦的两种晶体结构，标识符`YIGPIO01`和`YIGPIO02`.

要对分子进行分子几何分析，需要创建几何分析引擎。

```python
from ccdc import conformer
engine = conformer.GeometryAnalyser()
```

我们只对分析扭转角感兴趣，因此我们将关闭对键、价角和环的分析。在此示例中，我们还将关闭搜索泛化。

```python
engine.settings.bond.analyse = False
engine.settings.angle.analyse = False
engine.settings.ring.analyse = False
engine.settings.generalisation = False
```

为了便于分析，我们将使用一个简单的函数，该函数采用标识符列表并打印出标识符和结构中异常扭转角的数量。

```python
def conformation_analysis(identifiers):
    print('REFCODE, UnusualTorsions')
    with io.MoleculeReader('CSD') as reader:
        for identifer in identifiers:
            mol = reader.molecule(identifer)
            checked_mol = engine.analyse_molecule(mol)
            num_unusual = len([t for t in checked_mol.analysed_torsions if t.unusual])
            print("%s, %i" % (identifer, num_unusual))
...
```

该[`ccdc.conformer.GeometryAnalyser.analyse_molecule()`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/conformer_api.html#ccdc.conformer.GeometryAnalyser.analyse_molecule)函数返回一个 [`ccdc.molecule.Molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule)动态添加的属性列表，用于分析的特征，在本例中为`analysed_torsions`。这些列表包含`ccdc.conformer.Analysis`实例，其中包含诸如[`ccdc.conformer.GeometryAnalyser.Analysis.unusual`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/conformer_api.html#ccdc.conformer.GeometryAnalyser.Analysis.unusual). 我们可以用它来计算在晶体结构中观察到的异常扭转角的数量。

```python
conformation_analysis(['YIGPIO01', 'YIGPIO02'])
REFCODE, UnusualTorsions
YIGPIO01, 3
YIGPIO02, 0 
```

> 描述[性分子几何分析文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/conformer.html)和 [`ccdc.conformer`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/conformer_api.html#module-ccdc.conformer)API 文档。

## 5. 交互偏好分析

CSD 产品组合包含基于知识的分子间相互作用库。在本例中，我们将使用这些库来帮助我们了解在扑热息痛/对乙酰氨基酚 ( `HXACAN`) 的晶体结构中更可取的相互作用。

首先，我们创建中央和联系人组库。

```python
from ccdc.interaction import InteractionLibrary
central_lib = InteractionLibrary.CentralGroupLibrary()
contact_lib = InteractionLibrary.ContactGroupLibrary()
```

这些文库可用于识别扑热息痛分子中存在哪些中心基团和接触基团。

```python
paracetamol = csd_reader.molecule('HXACAN')
central_hits = central_lib.search_molecule(paracetamol)
contact_hits = contact_lib.search_molecule(paracetamol)
```

然后，我们可以遍历中心和接触组命中，以识别相对密度大于 1.0 的任何对。下面的代码需要一点时间才能完成。

```python
potential_interaction = []
for central_hit in central_hits: 
    for contact_hit in contact_hits:
        data = central_hit.group.interaction_data(contact_hit.group)
        if data is None:
            continue
        rel_density, est_std_dev = data.relative_density
        if rel_density > 2.0:
            interaction = (rel_density,
                           data.ncontacts,
                           central_hit.name,
                           [i+1 for i in central_hit.match_atoms(indices=True)],
                           contact_hit.name,
                           [i+1 for i in contact_hit.match_atoms(indices=True)])
            potential_interaction.append(interaction)
...
```

最后，我们按相互作用的相对密度对相互作用进行排序并打印出来。

```python
for interaction in sorted(potential_interaction, reverse=True):  
    print("%.2f | %i | %s %s | %s %s" % interaction)
...
3.82 | 949 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | any OH [19, 13]
3.00 | 112 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | phenol OH [3, 5, 4, 19, 13]
2.97 | 135 | acetylamino [1, 18, 7, 20, 8, 15, 16, 17, 14] | phenol OH [3, 5, 4, 19, 13]
2.79 | 2759 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | any polar X-H (X= N,O or S) [19, 13]
2.79 | 2759 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | any polar X-H (X= N,O or S) [18, 14]
2.54 | 1661 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | any uncharged N-H [18, 14]
2.53 | 1626 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | any uncharged N(sp2)-H [18, 14]
2.50 | 1535 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | uncharged C-NH-C [1, 7, 18, 14]
2.48 | 1429 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | amide N-H [8, 1, 7, 20, 18, 14]
2.41 | 1810 | aromatic-aliphatic amide [2, 6, 1, 8, 18, 7, 20, 14] | any N-H [18, 14]
```

![HXACAN 的原子索引。](https://downloads.ccdc.cam.ac.uk/documentation/API/_images/hxacan.png)

中的扑热息痛分子的原子指数`HXACAN`。

> 描述[性交互库文档](https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/interaction.html)和[`ccdc.interaction`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/interaction_api.html#module-ccdc.interaction)API 文档。


## 6. 访问条目(Entry)属性

https://downloads.ccdc.cam.ac.uk/documentation/API/descriptive_docs/entry.html#introduction

该[`ccdc.entry`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#module-ccdc.entry)模块包含[`ccdc.entry.Entry`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry) 代表数据库条目的类。

通常，将从 CSD 读取数据库条目。因此，让我们导入[`ccdc.io`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#module-ccdc.io)模块并从 CSD 中读取第一个条目。

```python
from ccdc import io
csd_reader = io.EntryReader('CSD')
first_csd_entry = csd_reader[0]
```

[入口模块的API文档](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html)


让我们看一下 CSD 晶体结构中可用的晶体学特性。

首先值得注意的是，人们可以访问底层证券[`ccdc.crystal.Crystal`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/crystal_api.html#ccdc.crystal.Crystal)并[`ccdc.molecule.Molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/molecule_api.html#ccdc.molecule.Molecule)从入口处访问。

```python
mol = first_csd_entry.crystal.molecule
print(mol.identifier)
AABHTZ
```

CSD 中的一些条目表现出混乱。默认情况下，[`ccdc.entry.Entry.molecule`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/entry_api.html#ccdc.entry.Entry.molecule)将抑制无序原子。例如，CSD 中的 'ABABUB' 就是这样一个条目：

```python
ababub = csd_reader.entry('ABABUB')
mol = ababub.molecule
print(len(mol.atoms))
30
print(mol.formula)
C12 H15 N1 O2
```

CSD 中的一个约定是无序原子的标签以“？”结尾。可以检索具有抑制原子的完整分子：

```python
disordered_mol = ababub.disordered_molecule
print(len(disordered_mol.atoms))
42
print(disordered_mol.formula)
C12 H15 N1 O2
```

对于已从 CSD 访问的条目，还可以访问晶体成分的化学名称和分子式。

```python
print(first_csd_entry.chemical_name)
4-Acetoamido-3-(1-acetyl-2-(2,6-dichlorobenzylidene)hydrazine)-1,2,4-triazole
print(first_csd_entry.formula)
C13 H12 Cl2 N6 O2
```

让我们使用布洛芬的晶体结构来说明 CSD 条目的更多可用属性。

```python
ibuprofen = csd_reader.entry('IBPRAC')
print(ibuprofen.has_3d_structure)
True
print(ibuprofen.has_disorder)
False
print(ibuprofen.is_organometallic)
False
print(ibuprofen.is_polymeric)
False
print(ibuprofen.bioactivity)
analgesic and antiinflammatory agent
print('\n'.join(ibuprofen.synonyms))
Ibuprofen
Advil
Motrin
Nurofen
DrugBank: DB01050
PDB Chemical Component code: IZP
```

此特定 CSD 条目没有发布 DOI。

```python
print(ibuprofen.publication.doi)
None
```

python但是，在它被定义的地方，它将被返回。

```python
print(csd_reader.entry('ABEBUF').publication.doi)
10.1021/cg049957u
print(csd_reader.entry('ABEBUF').publication)  
Citation(authors='S.W.Gordon-Wylie, E.Teplin, J.C.Morris, M.I.Trombley,
                   S.M.McCarthy, W.M.Cleaver, G.R.Clark',
         journal='Journal(Crystal Growth and Design)', volume='4', year=2004,
         first_page='789', doi='10.1021/cg049957u')
```

出版物以命名元组的形式返回，其成员可以按名称或索引检索，包含作者、期刊名称、卷、年份、第一页数和出版物的 doi（如果存在）。

```python
print(ibuprofen.publication)  
Citation(authors='J.F.McConnell',
         journal='Journal(Crystal Structure Communications)', volume='3', year=1974,
         first_page='73', doi=None)
print(ibuprofen.publication.authors)
J.F.McConnell
```

从 CSD 条目中，当这些信息在基础 CSD 条目中可用时，还可以获取有关晶体测定或沉积日期的颜色、熔点、多晶型描述、任何无序和辐射源的信息。

```python
print(ibuprofen.color)
None
print(ibuprofen.melting_point)
None
print(ibuprofen.polymorph)
polymorph 1
print(ibuprofen.disorder_details)
None
print(csd_reader.entry('ABABUB').disorder_details)
The cyclohexene ring is disordered over two sites with occupancies 0.5878:0.4122.
print(csd_reader.entry('ABINOR01').radiation_source)
Neutron
print(ibuprofen.deposition_date)
1974-06-21
```

布洛芬的条目没有编辑评论；如果它们出现，它们可能代表在结构管理或专利信息期间做出的编辑决定：

```python
print(ibuprofen.remarks)
None
print(csd_reader.entry('ABAPCU').remarks)
The position of the hydrate is dubious. It has been deleted
print(csd_reader.entry('ARISOK').remarks)
U.S. Patent: US 6858644 B2
```

可以提供有关是否在压力下进行实验的指示。这是作为字符串给出的，单位尚未标准化。如果这是无，则实验是在环境压力下进行的：

```python
print(ibuprofen.pressure)
None
print(csd_reader.entry('ABULIT03').pressure)
at 1.4 GPa
```

布尔属性将指示晶体学测定是否在粉末研究中进行：

```python
print(ibuprofen.is_powder_study)
False
print(csd_reader.entry('ACATAA').is_powder_study)
True
```

在 CSD 中，许多结构都被交叉引用。这些可以通过以下方式获得和检查：

```python
cross_refs = ibuprofen.cross_references
print(cross_refs)
(CrossReference(for stereoisomer see [JEKNOC]),)
xref = cross_refs[0]
print(xref.text)
for stereoisomer see [JEKNOC]
print(xref.type)
Stereoisomer
print(xref.scope)
Family
print(xref.identifiers)
('JEKNOC',)
```

这些属性不适用于从例如 mol2 文件中读取的条目。

```python
filepath = 'ABEBUF.mol2'
```

要访问此文件中的条目，我们使用 [`ccdc.io.EntryReader`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#ccdc.io.EntryReader).

```python
entry_reader = io.EntryReader(filepath)
entry_from_mol2 = entry_reader[0]
entry_reader.close()
print(entry_from_mol2.chemical_name)
None
print(entry_from_mol2.formula)
C19 H15 N3 O2
```

如果数据库来自 sdf 文件，EntryReader 将通过 entry.attributes 属性访问条目的 SDF 标签：

```python
file_name = 'gold_output.sdf'
```

要访问此文件中的条目，我们使用 [`ccdc.io.EntryReader`](https://downloads.ccdc.cam.ac.uk/documentation/API/modules/io_api.html#ccdc.io.EntryReader).

```python
reader = io.EntryReader(file_name)
entry_from_sdf = reader[0]
for k, v in sorted(entry_from_sdf.attributes.items()):
    print(k)
    print(v)
...
Gold.Chemscore.DEClash
17.1265
Gold.Chemscore.DEClash.Weighted
17.1265
Gold.Chemscore.DEInternal
2.1334
Gold.Chemscore.DEInternal.Weighted
2.1334
Gold.Chemscore.DG
-34.5350
Gold.Chemscore.Fitness
15.2752
Gold.Chemscore.Hbond
0.9975
Gold.Chemscore.Hbond.Weighted
-3.3317
Gold.Chemscore.Internal_Hbond
0.0000
Gold.Chemscore.Internal_Hbond.Weighted
0.0000
Gold.Chemscore.Lipo
257.3928
Gold.Chemscore.Lipo.Weighted
-30.1150
Gold.Chemscore.Metal
0.0000
Gold.Chemscore.Metal.Weighted
0.0000
Gold.Chemscore.Rot
1.7155
Gold.Chemscore.Rot.Weighted
4.3916
Gold.Chemscore.ZeroCoef
-5.4800
Gold.Protein.ActiveResidues
 PHE87   TYR96   PHE98   THR101  MET184  THR185  LEU244  VAL247  GLY248  THR252
 VAL295  ASP297  ILE395  VAL396  HEM1
Gold.Protein.RotatedAtoms
   42.8596   40.6557   11.7180 H   0  0  0  0  0  0  0  0  0  0  0  0  # atno 6359 bound_to 3214
   39.9356   46.2719   13.3012 H   0  0  0  0  0  0  0  0  0  0  0  0  # atno 6443 bound_to 742
reader.close()
```

属性 dict 的值都是字符串：留给用户酌情转换。

条目可以由具有从任意关键字参数构造的属性的分子构造。

```python
from ccdc.entry import Entry
aabhtz_entry = Entry.from_molecule(mol, annotation='First structure in CSD')
```

属性也可以在实例化后添加到条目中。

```python
aabhtz_entry.attributes['molecular_weight'] = mol.molecular_weight
```

请注意，可以将任何值的属性添加到条目中。如果使用 EntryWriter，这些属性将被写入 sdf 格式文件：

```python
with io.EntryWriter('aabhtz.sdf') as writer:
    writer.write(aabhtz_entry)
```