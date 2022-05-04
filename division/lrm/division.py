from reader import *
from writer import *
import networkx as nx


def divide_sub_structure(g):
    for n, nbrs in g.adj.items():
        if g.nodes[n]['type_symbol'] == 'C':
            ebunch_tmp = []
            C_num = 0
            O_num = 0
            for nbr in nbrs.keys():
                if g.nodes[nbr]['type_symbol'] == 'O':
                    O_num += 1
                elif g.nodes[nbr]['type_symbol'] == 'C':
                    C_num += 1
                    ebunch_tmp.append((n, nbr))
            if O_num == 2 and C_num == 1:
                g.remove_edges_from(ebunch_tmp)
    return g


def get_connected_subgraph(g):
    subgraph_list = []
    for c in nx.connected_components(g):
        subgraph_list.append(g.subgraph(c))
    return subgraph_list


if __name__ == '__main__':
    file_name = "division/2/MOF.cif"
    g = read_cif(file_name)
    g = divide_sub_structure(g)
    subgraph_list = get_connected_subgraph(g)
    for i in range(0, len(subgraph_list)):
        write_cif(subgraph_list[i], "outcome_" + str(i) + ".cif")
