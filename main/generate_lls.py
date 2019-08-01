import pandas as pd
from Genome.goldstandard_pair.lls import *

# wrap for domain
gd = '/home/hermuba/data0118/goldstandard/tf_intersect_pathway_rm_plasmid.smpl'
gold = read_gold(gd)

##### not finished

def wrap_for_diff_score(score, all_chunk):
    lls_score = lls_for_domain(all_chunk, score)
    true_thres, slope, intercept = lls_regress_thres(lls_score)
    new_lls = map_lls(lls_score, true_thres, slope, intercept)
    all_chunk = map_score_to_lls(all_chunk, new_lls, score)
    tradeoff = try_diff_lls_thres(all_chunk)
    return(new_lls, all_chunk,lls_score, tradeoff, true_thres)

all_df = pd.read_csv('~/data0118/goldstandard/GO_smpl/domain_GO_smpl', header = 0) # this step is f slow

new_lls, all_chunk,lls_score, tradeoff, true_thres = wrap_for_diff_score('weighted_mutual', all_df)

output = '/home/hermuba/data0118/network1122/domain_lls_edgelist'
net = '/home/hermuba/data0118/domain_weight_mutual'
# map LLS_reg back to each "whole" network
map_lls_to_whole_data(net, new_lls, 'weighted_mutual', true_thres, output, 'domain')


# wrap for other

def wrap_for_diff_score(score, all_chunk):
    lls_score = lls_for_other(all_chunk, score)
    true_thres, slope, intercept = lls_regress_thres(lls_score)
    new_lls = map_lls(lls_score, true_thres, slope, intercept)
    all_chunk = map_score_to_lls(all_chunk, new_lls, score)
    tradeoff = try_diff_lls_thres(all_chunk)
    return(new_lls, all_chunk,lls_score, tradeoff, true_thres)

# eskape
all_chunk = pd.read_csv('~/data0118/goldstandard/GO_smpl/eskape_GO_smpl', header = 0)
new_lls, all_chunk,lls_score, tradeoff, true_thres = wrap_for_diff_score('nrm_mutual', all_chunk)
output = '/home/hermuba/data0118/network1122/eskape_lls_edgelist'
# map LLS_reg back to each "whole" network
net = '/home/hermuba/data0118/mutual_info/eskape_blastp_out_max_evalue_ordinary_mutual'
map_lls_to_whole_data(net, new_lls, 'nrm_mutual', true_thres, output, 'eskape')

# refseq
all_chunk = pd.read_csv('~/data0118/refseq_GO_smpl', header = 0)
new_lls, all_chunk,lls_score, tradeoff, true_thres = wrap_for_diff_score('nrm_mutual', all_chunk)
output = '/home/hermuba/data0118/network1122/refseq_lls_edgelist'
net = '/home/hermuba/data0118/mutual_info//blastp_out_max_evalue_oridinary40_mutual'
# map LLS_reg back to each "whole" network
map_lls_to_whole_data(net, new_lls, 'nrm_mutual', true_thres, output, 'refseq')

# string
all_chunk = pd.read_csv('~/data0118/string_GO_smpl', header = 0)
new_lls, all_chunk,lls_score, tradeoff, true_thres = wrap_for_diff_score('combined_score', all_chunk)
output = '/home/hermuba/data0118/network1122/string_lls_edgelist'
net = '/home/hermuba/data0118/map_to_exist_net/string' #ID has problem
map_lls_to_whole_data(net, new_lls, 'combined_score', true_thres, output, 'string')
