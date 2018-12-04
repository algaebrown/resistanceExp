# a script to download genomes
genome_path = "/home/hermuba/data/genome/"
gene_path = "/home/hermuba/data0118/predicted_genes/"
genome_list = "/home/hermuba/data0118/genomeList/all"

id_list = []
with open(genome_list, "r") as f:
    for ID in f.readlines():
        id_list.append(ID.replace('\n',''))

import os
from os.path import isfile, join
onlyfiles = [f.replace(".fna", '') for f in os.listdir(genome_path) if isfile(join(genome_path, f))]

for i in id_list:
    if i not in onlyfiles:
        os.chdir(genome_path)
        os.system("wget ftp://ftp.patricbrc.org/genomes/"+i+"/"+i+".fna")
    else:
        print("already have")
