import networkx as nx
from pymatgen.io.cif import CifParser


def read_cif(file_name):
    parser = CifParser(file_name)
    cif_dict = list(parser.as_dict().values())[0]

    graph_attr_dict_key_set = {"_audit_creation_date",
                               "_audit_creation_method",
                               "_symmetry_space_group_name_H-M",
                               "_symmetry_Int_Tables_number",
                               "_symmetry_cell_setting",
                               "_symmetry_equiv_pos_as_xyz",
                               "_cell_length_a",
                               "_cell_length_b",
                               "_cell_length_c",
                               "_cell_angle_alpha",
                               "_cell_angle_beta",
                               "_cell_angle_gamma"}
    graph_attr_dict = {key: value for key, value in cif_dict.items() if key in graph_attr_dict_key_set}
    g = nx.Graph(cif_header_dict=graph_attr_dict)

    site_label_list = cif_dict.get("_atom_site_label")
    site_type_symbol_list = cif_dict.get("_atom_site_type_symbol")
    site_fract_x_list = cif_dict.get("_atom_site_fract_x")
    site_fract_y_list = cif_dict.get("_atom_site_fract_y")
    site_fract_z_list = cif_dict.get("_atom_site_fract_z")
    site_U_iso_or_equiv_list = cif_dict.get("_atom_site_U_iso_or_equiv")
    site_adp_type_list = cif_dict.get("_atom_site_adp_type")
    site_occupancy_list = cif_dict.get("_atom_site_occupancy")

    site_num = len(site_label_list)
    for i in range(0, site_num):
        node_attr_dict = {
            "_atom_site_label": site_label_list[i],
            "_atom_site_type_symbol": site_type_symbol_list[i],
            "_atom_site_fract_x": site_fract_x_list[i],
            "_atom_site_fract_y": site_fract_y_list[i],
            "_atom_site_fract_z": site_fract_z_list[i],
            "_atom_site_U_iso_or_equiv": site_U_iso_or_equiv_list[i],
            "_atom_site_adp_type": site_adp_type_list[i],
            "_atom_site_occupancy": site_occupancy_list[i]
        }
        g.add_node(site_label_list[i], type_symbol=site_type_symbol_list[i], site_attr_dict=node_attr_dict)

    bond_list = []
    bond_site_label1_list = cif_dict.get("_geom_bond_atom_site_label_1")
    bond_site_label2_list = cif_dict.get("_geom_bond_atom_site_label_2")
    bond_distance_list = cif_dict.get("_geom_bond_distance")
    bond_site_symmetry_list = cif_dict.get("_geom_bond_site_symmetry_2")
    bond_type_list = cif_dict.get("_ccdc_geom_bond_type")

    bond_num = len(bond_site_label1_list)
    for i in range(0, bond_num):
        bond_attr_dict = {
            "_geom_bond_atom_site_label_1": bond_site_label1_list[i],
            "_geom_bond_atom_site_label_2": bond_site_label2_list[i],
            "_geom_bond_distance": bond_distance_list[i],
            "_geom_bond_site_symmetry_2": bond_site_symmetry_list[i],
            "_ccdc_geom_bond_type": bond_type_list[i]
        }
        bond_list.append((bond_site_label1_list[i], bond_site_label2_list[i], {"bond_attr_dict": bond_attr_dict}))
    g.add_edges_from(bond_list)
    return g
