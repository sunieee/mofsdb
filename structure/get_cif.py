from ccdc import io
import os
csd_reader = io.EntryReader('CSD')
identifiers = ["ABAVIJ", 'ABEBUF','ABIYIV']

with open("/mnt/data1/csd/CCDC/CSD_2022/csd/subsets/CSD_MOF_subsets/Non-disordered_MOF_subset.gcd", 'r') as f:
    MOFS = f.readlines()

def get_cif():
    for MOF in MOFS:
        MOF = MOF.strip()
        print(MOF)
        filename = f"/mnt/data1/csd/cif/all/{MOF}.cif"
        if not os.path.exists(filename):
            entry = csd_reader.entry(MOF)
            with open(filename, "w") as f:
                f.write(entry.to_string("cif"))

if __name__ == "__main__":
    get_cif()
