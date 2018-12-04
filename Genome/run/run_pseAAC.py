#!/home/hermuba/miniconda3/envs/py27/bin/python
from propy.PyPro import GetProDes
import sys


def get_pseAAC(seq):
    Des = GetProDes(seq)
    return(Des.GetPAAC(lamda = 30, weight = 0.05)) # a dictionary

from Bio import SeqIO
import pandas as pd
#cluster_no = sys.argv[1] # pseAAC.py Cluster 9
def run_clus(cluster_no):
    clus = SeqIO.parse("/home/hermuba/data/genePredicted/cdhit/cluster_seq/Cluster "+cluster_no+".faa", "fasta")

    df = pd.DataFrame()
    for seq_record in clus:
        pse_dict = get_pseAAC(str(seq_record.seq).replace('*', ''))
        gene_id = seq_record.id
        pse_dict['id'] = gene_id
        df = df.append(pse_dict, ignore_index = True)
        print "done with" + str(gene_id)

    df = df.set_index('id')
    df.to_pickle("/home/hermuba/data/genePredicted/cdhit/cluster_pseAAC/"+cluster_no)

with open("cluster_selected") as f:
     l = f.readlines()
     for i in l:
        run_clus(i.replace('\n', ''))


