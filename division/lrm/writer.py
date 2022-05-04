from pymatgen.io.cif import CifBlock


def write_cif(g, file_path):
    cif_dict = g.graph["cif_header_dict"]

    site_label_list = []
    site_type_symbol_list = []
    site_fract_x_list = []
    site_fract_y_list = []
    site_fract_z_list = []
    site_U_iso_or_equiv_list = []
    site_adp_type_list = []
    site_occupancy_list = []
    for n in g.nodes:
        site_attr_dict = g.nodes[n]["site_attr_dict"]
        site_label_list.append(site_attr_dict['_atom_site_label'])
        site_type_symbol_list.append(site_attr_dict['_atom_site_type_symbol'])
        site_fract_x_list.append(site_attr_dict['_atom_site_fract_x'])
        site_fract_y_list.append(site_attr_dict['_atom_site_fract_y'])
        site_fract_z_list.append(site_attr_dict['_atom_site_fract_z'])
        site_U_iso_or_equiv_list.append(site_attr_dict['_atom_site_U_iso_or_equiv'])
        site_adp_type_list.append(site_attr_dict['_atom_site_adp_type'])
        site_occupancy_list.append(site_attr_dict['_atom_site_occupancy'])
    cif_dict['_atom_site_label'] = site_label_list
    cif_dict['_atom_site_type_symbol'] = site_type_symbol_list
    cif_dict['_atom_site_fract_x'] = site_fract_x_list
    cif_dict['_atom_site_fract_y'] = site_fract_y_list
    cif_dict['_atom_site_fract_z'] = site_fract_z_list
    cif_dict['_atom_site_U_iso_or_equiv'] = site_U_iso_or_equiv_list
    cif_dict['_atom_site_adp_type'] = site_adp_type_list
    cif_dict['_atom_site_occupancy'] = site_occupancy_list

    bond_site_label1_list = []
    bond_site_label2_list = []
    bond_distance_list = []
    bond_site_symmetry_list = []
    bond_type_list = []
    for e in g.edges:
        bond_attr_dict = g.edges[e]['bond_attr_dict']
        bond_site_label1_list.append(bond_attr_dict['_geom_bond_atom_site_label_1'])
        bond_site_label2_list.append(bond_attr_dict['_geom_bond_atom_site_label_2'])
        bond_distance_list.append(bond_attr_dict['_geom_bond_distance'])
        bond_site_symmetry_list.append(bond_attr_dict['_geom_bond_site_symmetry_2'])
        bond_type_list.append(bond_attr_dict['_ccdc_geom_bond_type'])
    cif_dict['_geom_bond_atom_site_label_1'] = bond_site_label1_list
    cif_dict['_geom_bond_atom_site_label_2'] = bond_site_label2_list
    cif_dict['_geom_bond_distance'] = bond_distance_list
    cif_dict['_geom_bond_site_symmetry_2'] = bond_site_symmetry_list
    cif_dict['_ccdc_geom_bond_type'] = bond_type_list

    cif_block = CifBlock(cif_dict,
                         [['_symmetry_equiv_pos_as_xyz'],
                          ['_atom_site_label',
                           '_atom_site_type_symbol',
                           '_atom_site_fract_x',
                           '_atom_site_fract_y',
                           '_atom_site_fract_z',
                           '_atom_site_U_iso_or_equiv',
                           '_atom_site_adp_type',
                           '_atom_site_adp_type',
                           '_atom_site_occupancy'],
                          ['_geom_bond_atom_site_label_1',
                           '_geom_bond_atom_site_label_2',
                           '_geom_bond_distance',
                           '_geom_bond_site_symmetry_2',
                           '_ccdc_geom_bond_type']],
                         '3D\Atomistic')
    file = open(file_path, "w")
    file.write(cif_block.__str__())
