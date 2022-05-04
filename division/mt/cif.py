from typing import List
import os


class Cif:

    def __init__(self):
        self.title = ''
        self.file_info = []
        self.symmetry_info = []
        self.atoms_info = []
        self.atoms_idx = {}
        self.atoms = []
        self.bonds_info = []
        self.bonds_map = {}
        self.bonds = []
        self.g = []

    def parse_file(self, file: str):
        # try:
        with open(file, 'r') as f:
            lines = list(f.readlines())
        
        line_num = self.read_file_info(lines)
        line_num = self.read_symmetry_info(lines, line_num)
        line_num = self.read_atom_info(lines, line_num)
        self.read_bond_info(lines, line_num)
        # except Exception as e:
        #     print(e)

    @staticmethod
    def _is_property(s: str) -> bool:
        return s[0] == '_'

    @staticmethod
    def _loop_end(s: str) -> bool:
        return not s.startswith('loop_')

    def read_file_info(self, lines: List[str]):
        self.title = lines[0]
        line_num = 1
        while line_num < len(lines) and Cif._is_property(lines[line_num]):
            self.file_info.append(lines[line_num])
            line_num += 1
        return line_num

    def read_symmetry_info(self, lines: List[str], line_num: int):
        line_num += 1
        while line_num < len(lines) and Cif._loop_end(lines[line_num]):
            self.symmetry_info.append(lines[line_num])
            line_num += 1
        return line_num

    def read_atom_info(self, lines: List[str], line_num: int):
        line_num += 1  # ignore loop_
        while line_num < len(lines) and Cif._is_property(lines[line_num]):
            self.atoms_info.append(lines[line_num])
            line_num += 1
        idx = 0
        while line_num < len(lines) and Cif._loop_end(lines[line_num]):
            values = lines[line_num].split()
            atom = Atom()
            for k, v in zip(self.atoms_info, values):
                setattr(atom, k, v)
            atom.from_string(lines[line_num], self.atoms_info)
            self.atoms.append(atom)
            self.atoms_idx[atom.label] = idx
            idx += 1
            line_num += 1

        return line_num

    def read_bond_info(self, lines: List[str], line_num: int):
        line_num += 1  # ignore loop_
        while line_num < len(lines) and Cif._is_property(lines[line_num]):
            self.bonds_info.append(lines[line_num])
            line_num += 1
        while line_num < len(lines) and Cif._loop_end(lines[line_num]):
            values = lines[line_num].split()
            bond = Bond()
            for k, v in zip(self.bonds_info, values):
                setattr(bond, k, v)
            bond.from_string(lines[line_num], self.bonds_info)
            self.bonds.append(bond)
            self.bonds_map[(bond.site1, bond.site2)] = bond
            line_num += 1
        return line_num

    def _build_graph(self):
        n = len(self.atoms)
        g = [[0] * n for _ in range(n)]

        labels = self.atoms_idx
        for bond in self.bonds:
            s1, s2 = bond.site1, bond.site2
            g[labels[s1]][labels[s2]] = 1
            g[labels[s2]][labels[s1]] = 1

        self.g = g

    def _need_break(self, idx: int):
        if self.atoms[idx].element != 'C':
            return False, -1

        n = len(self.atoms)
        c_num, o_num, c_idx = 0, 0, -1
        for i in range(n):
            if self.g[idx][i]:
                atom = self.atoms[i]
                if atom.element == 'C':
                    c_num += 1
                    c_idx = i
                if atom.element == 'O':
                    o_num += 1
        return c_num == 1 and o_num == 2, c_idx

    def _break_bond(self):
        n = len(self.atoms)
        for i in range(n):
            flag, c_id = self._need_break(i)
            if flag:
                self.g[i][c_id] = 0
                self.g[c_id][i] = 0

    def _generate_cif(self, s: List):
        cif = Cif()
        cif.title = self.title.split()[0] + 'piece\n'
        cif.file_info = self.file_info
        cif.symmetry_info = self.symmetry_info
        cif.atoms_info = self.atoms_info
        cif.atoms = s
        cif.bonds_info = self.bonds_info
        bonds = []
        for f in s:
            idx = self.atoms_idx[f.label]
            for j, t in enumerate(self.atoms):
                if self.g[idx][j] and (f.label, t.label) in self.bonds_map.keys():
                    bonds.append(self.bonds_map[(f.label, t.label)])
        cif.bonds = bonds

        # cnt, mp = 1, {}
        # for atom in cif.atoms:
        #     label = atom.element + str(cnt)
        #     cnt += 1
        #     mp[atom.label] = label
        #     atom.label = label
        #
        # for bond in cif.bonds:
        #     bond.site1 = mp[bond.site1]
        #     bond.site2 = mp[bond.site2]
        return cif

    def _divide(self):
        self._build_graph()
        self._break_bond()
        n = len(self.atoms)
        vis = set()

        def dfs(idx: int, s: List):
            if idx in vis:
                return s
            vis.add(idx)
            s.append(self.atoms[idx])
            for j in range(n):
                if self.g[idx][j]:
                    dfs(j, s)
            return s

        pieces = []
        for i in range(n):
            piece = []
            dfs(i, piece)
            if piece:
                pieces.append(piece)

        cifs = []
        for p in pieces:
            cif = self._generate_cif(p)
            cifs.append(cif)

        return cifs

    def generate_cif(self, folder):
        cifs = self._divide()
        for i, cif in enumerate(cifs):
            os.makedirs(folder, exist_ok=True)
            with open(f'{folder}/cif_{i}.cif', 'w') as f:
                f.write(cif.title)
                print(cif.title)
                f.writelines(cif.file_info)
                f.write('loop_\n')
                f.writelines(cif.symmetry_info)
                f.write('loop_\n')
                f.writelines(cif.atoms_info)
                f.writelines(Atom.list_to_string(cif.atoms, cif.atoms_info))
                print(Atom.list_to_string(cif.atoms, cif.atoms_info))
                f.write('loop_\n')
                f.writelines(cif.bonds_info)
                f.writelines(Bond.list_to_string(cif.bonds, cif.bonds_info))


class Atom:

    def __init__(self):
        self.element = ''
        self.label = ''
        self.position = []

    def from_string(self, s: str, attr: List[str]):
        values = s.split()
        position = [0] * 3
        for k, v in zip(attr, values):
            if 'symbol' in k:
                self.element = v
            elif 'fract_x' in k:
                position[0] = v
            elif 'fract_y' in k:
                position[1] = v
            elif 'fract_z' in k:
                position[2] = v
            elif 'label' in k:
                self.label = v
        self.position = position

    @staticmethod
    def list_to_string(atoms, attrs):
        lines = []
        for atom in atoms:
            val = []
            for attr in attrs:
                val.append(getattr(atom, attr))
            lines.append('\t'.join(val) + '\n')
        return lines


class Bond:

    def __init__(self):
        self.site1 = None
        self.site2 = None

    def from_string(self, s: str, attr: List[str]):
        values = s.split()
        for k, v in zip(attr, values):
            if 'label_1' in k:
                self.site1 = v
            elif 'label_2' in k:
                self.site2 = v

    @staticmethod
    def list_to_string(bonds, attrs):
        lines = []
        for bond in bonds:
            val = []
            for attr in attrs:
                val.append(getattr(bond, attr))
            lines.append('\t'.join(val) + '\n')
        return lines


if __name__ == '__main__':
    path = 'MOF.cif'
    c = Cif()
    c.parse_file(path)
    c.generate_cif('output')
    print(c)

