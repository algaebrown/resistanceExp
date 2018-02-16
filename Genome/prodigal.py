# a script to run prodigal gene prediction on all the genomes
import os

# set path of all genome and path of output `gene_path`
genome_path = "/home/hermuba/data/genome/"
gene_path = "/home/hermuba/data0118/predicted_genes/"
genome_list = "/home/hermuba/data0118/genomeList/all"

def run(ID):
    print("running prodigal for " + ID)
    os.system("prodigal -i "+ genome_path + ID + ".fna -o "+gene_path+ID+".gbk -a "+gene_path+ID+".faa" + " -p meta")



id_list = []
with open(genome_list, "r") as f:
    for ID in f.readlines():
        id_list.append(ID.replace('\n',''))
from multiprocessing import Pool
with Pool(5) as p:
    print(p.map(run, id_list))
