# read in all genome
with open("/home/hermuba/data/genomeList/ECgenome.txt") as f:
    g_list = f.readlines()
for i in range(len(g_list)):
    g_list[i] = g_list[i].replace('\n', '')

# run quast for genome stats
import os
for genome_id in g_list:
    os.system("/home/hermuba/bin/quast/quast.py "+"/home/hermuba/data/genome/"+genome_id+'.fna '+'-o /home/hermuba/data/genome/genome_stat/'+genome_id)

# parse quast output file
import pandas as pd

# a function to parse report.txt from quast
path = '/home/hermuba/data/genome/genome_stat/'

def parse_quast(s):
    with open(s) as f:
        file_list = f.readlines()
    length = file_list[9].replace('Total length (>= 0 bp)', '').replace(' ', '').replace('\n', '')
    N_fifty = file_list[19].replace(' ', '').replace('\n', '').replace('N50', '')
    return(length,N_fifty)

n_list = []
genome_length = []
for genome in g_list:
    l,N = parse_quast(path + genome + '/report.txt')
    n_list.append(float(N))
    genome_length.append(float(l))
df = pd.DataFrame(n_list, index = g_list)
df['Genome Length'] = genome_length
df.to_excel("/home/hermuba/data/n50.xlsx")
