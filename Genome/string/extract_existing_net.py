# import module written for processing our gene mapping to gene ID, filter with e-value, pident
from network_analysis.map_string_to_ID import *
import sys
import os


# node_path referes to diamond blastp --in REPRESENTING GENE --db string.dmnd
network_seq_path = sys.argv[1] 
edge_path = sys.argv[2]
gold_anno_path = sys.argv[3]
network_name = sys.argv[4]
repr_faa = sys.argv[5]
outdir = sys.argv[6]
header = sys.argv[7]

# create ID mapper
os.system('diamond makedb --in {} --db {}'.format(network_seq_path, network_name))
try:
    os.mkdir(os.path.join(outdir, network_name))
except:
    print('path exists')
node_mapper = os.path.join(outdir, network_name, 'node_mapper.blast')
os.system('diamond blastp --query {} --db {} --outfmt 6 --out {}'.format(repr_faa, network_name+'.dmnd', node_mapper))

os.system('rm {}.dmnd'.format(network_name))

# read in the result
node = read_node_to_df(node_mapper)
# select nodes with high bitscore with string 511145 proteins
selected_nodes = filter_node(node)

# read in STRING edges
if header == '1':
    edge = string_edge_to_df(edge_path)
else:
    edge = pd.read_csv(edge_path, sep = '\t', header = None, names = ['Protein A', 'Protein B', 'Score'])

print(selected_nodes.head())
selected_edge = map_string_to_repr(edge, selected_nodes)

print(selected_edge.head(), edge.shape)

# replace selected_edge with gene_id
gold_anno = pd.read_csv(gold_anno_path, index_col = 0, header = 0)
selected_edge['gene_one'] = selected_edge['gene_one'].map(gold_anno['gene_id'])
selected_edge['gene_two'] = selected_edge['gene_two'].map(gold_anno['gene_id'])


# output
selected_edge[['gene_one', 'gene_two', 'combined_score']].to_csv(os.path.join(outdir, network_name, 'network.csv'), index = False, header = False)



