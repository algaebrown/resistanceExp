# card_net: all genes with edges with card genes
import pandas as pd

card_net = '/home/hermuba/data0118/network1122/card_lls' # no header
net = pd.read_csv(card_net, index_col = 0, names = ['gene_one', 'gene_two', 'combined_lls']) # 40000 lines

# annotation =
gold_anno = pd.read_csv('/home/hermuba/data0118/network1122/gold_anno.csv', header = 0, index_col = 0)

# form network by networkx
import networkx as nx
card_net = nx.convert_matrix.from_pandas_edgelist(net, 'gene_one', 'gene_two', edge_attr = 'combined_lls')

# generate adjacency matrix
adj = nx.convert_matrix.to_pandas_adjacency(card_net, weight = 'combined_lls')

# identify card genes
card_index = gold_anno.loc[gold_anno['is_card']==True].index
non_card_index = set(adj.index) - set(gold_anno.loc[gold_anno['is_card']==True].index)

# identify resfam index
resfam_index = gold_anno.loc[gold_anno['resfam'].notnull()].index
missed_resfam = set(resfam_index) - set(adj.index)
included_resfam = set(resfam_index).intersection(set(adj.index))

# card-card similarity
card = adj.loc[card_index, card_index].mean()

# card-all_other
candidates = adj.loc[card_index, non_card_index].mean(axis = 0)

# resfam
resfam = adj.loc[card_index, included_resfam].mean(axis = 0)

# passed candidate
passed = candidates.loc[candidates > card.mean()].index

# how many passed are resfam genes
included_and_res = set(passed).intersection(included_resfam)
