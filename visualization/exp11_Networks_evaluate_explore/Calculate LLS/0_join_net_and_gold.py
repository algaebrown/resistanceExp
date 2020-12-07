# This script is to join network and goldstandard for calculation of LLS scores.

# load module
import pandas as pd
from Genome.goldstandard_pair.lls import *


# load gold standard network
gd = '/home/hermuba/data0118/goldstandard/tf_intersect_GO_rm_plasmidGO.smpl'
gold= read_gold(gd)


# load each network, join, and save as csv for later analysis


############### DOMAIN NET ###############################
net = '/home/hermuba/data0118/domain/domain_rm_plasmid_weighted_mutual'
all_chunks = read_net_by_chunk(net)
all_df = merge_net_with_all_chunks(gold, all_chunks)
# save joined sample to edgelist
all_df.to_csv('~/data0118/joined_smpl/domain_GO_smpl_rm_plasmid')


############### ESKAPE NET ###############################
net = '/home/hermuba/data0118/mutual_info/eskape_blastp_out_max_evalue_pivot_new_ordinary40_mutual' 
all_chunks = read_net_by_chunk(net)
all_df = merge_net_with_all_chunks(gold, all_chunks)
# save joined sample to edgelist
all_df.to_csv('~/data0118/joined_smpl/eskape_GO_smpl_rm_plasmid')

############### REFSEQ NET ###############################
net = '/home/hermuba/data0118/mutual_info/blastp_out_max_evalue_pivot_new_ordinary40_mutual' #ID has problem
all_chunks = read_net_by_chunk(net)
all_chunk = merge_net_with_all_chunks(gold,all_chunks)
all_chunk.to_csv('~/data0118/refseq_GO_smpl_rm_plasmid')

################ STRING #################################