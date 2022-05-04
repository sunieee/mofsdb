from ccdc import io
import os
csd_reader = io.EntryReader('CSD')
identifiers = ["ABAVIJ", 'ABEBUF','ABIYIV']

with open("/mnt/data1/csd/CCDC/CSD_2022/csd/subsets/CSD_MOF_subsets/Non-disordered_MOF_subset.gcd", 'r') as f:
    MOFS = f.readlines()

# print(len(MOFS))

def to_str(dic):
    s = "{"
    for k, v in dic.items():
        if type(v) == dict:
            v = to_str(v)
            s += "\"%s\":%s," % (k, v)
        elif v is None:
            s += "\"%s\":null," % k
        elif type(v) == bool:
            s += "\"%s\":%s," % (k, str(v).lower())
        else:
            s += "\"%s\":\"%s\"," % (k, str(v).replace("\"", "'"))
    if s[-1] == ",":
        s = s[:-1]
    return s + "}"


def todic(identifier, simple=False):
    data  = {
        "entry": csd_reader.entry(identifier),
        "crystal": csd_reader.crystal(identifier),
        "molecule": csd_reader.molecule(identifier)
    }
    # print(dir(entry_abebuf))
    # print(entry_abebuf.has_3d_structure)

    dic = {
        'entry': {},
        'crystal': {},
        'molecule': {}
    }

    for t in dic:
        print(f"==================={t}===================")
        target = data[t]
        for k in dir(target):
            if k.startswith(('_', 'delete')):
                continue
            if simple and k in ['heavy_atoms', 'atoms', 'bonds']:  # 二次过滤
                continue
            try:
                v = getattr(target, k)
                if str(v).startswith(('<class','<bound method','<function', '<ccdc.', '[<ccdc.')):
                    continue
                dic[t][k] = v
                # print(k,":", getattr(target, k))
            except:
                pass
    
    if simple:
        dic = {
            **dic['entry'],
            **dic['crystal'],
            **dic['molecule']
        }
        dic["doi"] = dic["publication"].doi
    return dic



# with open('saved_dictionary.pkl', 'rb') as f:
#     loaded_dict = pickle.load(f)

# print(type(entry_abebuf.delete_SolubilityInfo) )

# print(type(crystal_abebuf.Contact))
# print(type(crystal_abebuf.Contact))

def get_dic(simple=False):
    path = 'simple' if simple else 'all'
    for MOF in MOFS:
        MOF = MOF.strip()
        print(MOF)
        filename = f"/mnt/data1/csd/json/{path}/{MOF}.json"
        if not os.path.exists(filename):
            dic = todic(MOF, simple)
            with open(filename, 'w') as f:
                f.write(to_str(dic))


def get_cif():
    for MOF in MOFS:
        MOF = MOF.strip()
        print(MOF)
        filename = f"/mnt/data1/csd/cif/all/{MOF}.cif"
        if not os.path.exists(filename):
            entry = csd_reader.entry(MOF)
            with open(filename, "w") as f:
                f.write(entry.to_string("cif"))


def generate_example(identifier):
    dic = todic(identifier)
    with open('all.json', 'w') as f:
        f.write(to_str(dic))

    dic = todic(identifier, True)
    with open('simple.json', 'w') as f:
        f.write(to_str(dic))


def get_smiles(MOF):
    import json
    filename = f"/mnt/data1/csd/json/all/{MOF}.json"
    with open(filename) as f:
        dic = json.load(f)
        if dic['molecule']['smiles'] is not None:
            print(dic['molecule']['smiles'])
        return dic['molecule']['smiles']

if __name__ == "__main__":
    # generate_example(identifiers[0])
    # get_dic(False)
    # get_dic(True)
    # get_cif()
    for MOF in MOFS:
        get_smiles(MOF.strip())
