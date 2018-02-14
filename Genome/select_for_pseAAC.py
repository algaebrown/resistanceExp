# select clusters for pseAAC experiment

import pandas as pd
# read blast file
blast = pd.read_pickle("/home/hermuba/data/blast/blastp_gi_1022")
lactamase = blast.loc[blast['title'].str.contains('lactamase')]
efflux_pump = blast.loc[blast['title'].str.contains('efflux')]
pbp = blast.loc[blast['title'].str.contains('penicillin')]

# read cluster detail
cluster_detail = pd.read_pickle("/home/hermuba/data/genePredicted/cdhit/cluster_detail_df")

# return cluster name
l = cluster_detail.loc[cluster_detail['representing gene header'].isin(lactamase.index)].index
e = cluster_detail.loc[cluster_detail['representing gene header'].isin(efflux_pump.index)].index
p = cluster_detail.loc[cluster_detail['representing gene header'].isin(pbp.index)].index

#
list_clus = list(l) + list(e) + list(p)
for i in list_clus:
    with open("cluster_selected", 'a') as f:
        f.write(i.split(' ')[1]+'\n') # cluster_no
