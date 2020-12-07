# make dmnd for string protein sequence 511145.protein.sequence

# blast representing gene to 511145.protein.sequence

import pandas as pd
# parse diamond output file
def read_node_to_df(fname):
    '''
    input: diamond blastp --query REPRESETING_GENE --db STRING.dmnd --outfmt 6
    output: dataframe with essential info: qseqid, sseqid, pident, evalue
    '''
    node = pd.read_csv(fname, sep = '\t', header = None)
    node = node[[0,1,2,10]]
    node = node.rename(columns = {0:'qseqid', 1:'sseqid', 2:'pident', 10:'evalue'})
    return(node)

# filter nodes
def filter_node(node):
    '''
    input: node dataframe from `read_node_to_df
    output: filtered net
    steps:
    1. select max pident for each sseqid(STRING ID)
    2. remove all hits with pident < 70
    '''
    max_node = node[node.groupby(['sseqid'])['pident'].transform(max) == node['pident']]
    selected_nodes = max_node.loc[max_node['pident']>= 70]
    return(selected_nodes)

# change string ID to our ID
def string_edge_to_df(fname, sep = ' '):
    '''
    input: 511145.protein.links
    output: df with title "protein 1, protein2, combined score"
    '''
    edge = pd.read_csv(fname, sep = sep)
    return(edge)

def map_string_to_repr(edge, selected_nodes, output, target1 = 'protein1', target2 = 'protein2'):
    '''
    input: edge and node from `read_edge/node_to_df` and subsepquent processing
    output: edge table with additional columns gene_one, gene_two; representing gene ids
    '''
    edge['gene_one'] = edge[target1].map(selected_nodes['qseqid'])
    edge['gene_two'] = edge[target2].map(selected_nodes['qseqid'])

    edge.dropna(how = 'any', inplace = True) # we do not need interaction between genes that does not exist in our net

    # drop useless columns
    edge.drop(labels = [target1, target2], axis = 1, inplace = True)
    edge.to_csv(output, index = False, header = True)
    return(edge)
