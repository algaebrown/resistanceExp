# input: cluster_detail
# output: clusterX.faa with all members of a cluster with sequence info inside

# read file
import pandas as pd
cluster_detail = pd.read_pickle("/home/hermuba/data/genePredicted/cdhit/cluster_detail_df")

# import biopython
from Bio import SeqIO

# for each cluster, parse member
for index, row in cluster_detail.iterrows():
    members = row['member'].split(',')
    members = members[1:] # first item is empty
    with open("/home/hermuba/data/genePredicted/cdhit/cluster_seq/"+index+'.faa', "w") as f:
        for m in members: # one gene
            gene_id = m.split('|')[1]
            protein = m.split('|')[0]
            record_dict = SeqIO.to_dict("/home/hermuba/data/genePredicted/"+gene_id+'.faa', "fasta")
            SeqIO.write(record_dict[protein], f, "fasta")


# for each member, read the fasta
# write to file
