# import module written for processing our gene mapping to gene ID, filter with e-value, pident
from network_analysis.map_string_to_ID import *

# node_path referes to diamond blastp --in REPRESENTING GENE --db string.dmnd
node_path = '/home/hermuba/data0118/map_to_exist_net/ec_rmplasmid_string'
node = read_node_to_df(node_path)

# select nodes with high bitscore with string 511145 proteins
selected_nodes = filter_node(node)

# read the edge
edge_path = '/home/hermuba/data0118/map_to_exist_net/511145.protein.links.full.v11.0.txt'
edge = string_edge_to_df(edge_path)


# select edge with experiments != 0
#exp = edge.loc[edge['experiments']] == 1


# filter edge with both representing genes
output_path = '/home/hermuba/data0118/map_to_exist_net/string_rm_plasmid'
selected_edge = map_string_to_repr(edge, selected_nodes, output_path)
