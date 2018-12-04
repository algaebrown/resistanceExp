# path
clstr_path = "/home/hermuba/data/genePredicted/cdhit/ec0102.clstr"
save_path = "/home/hermuba/data/cdhitResult/cluster_comp/"
import pandas as pd

# read line by line
f = open(clstr_path)
cluster = 'Cluster 0'
df = pd.DataFrame(columns = ['length', 'gene_name', 'ID'])
for line in f:
    if line[0] == '>': # a new cluster
        df.to_pickle(save_path + cluster)
        df = pd.DataFrame(columns = ['length', 'gene_name', 'ID'])
        cluster = line.rstrip()[1:]
        print("reading", cluster)
        i = 0
    else:
        length = int(line.split('\t')[1].split('aa')[0])
        gene_name = line.split('|')[0].split('>')[1]
        ID = line.split('|')[1].split('...')[0]
        # save into dataframe
        df.append([length,gene_name, ID])
        i += 1
# saving the last cluster
df.to_pickle(save_path + cluster)

f.close()
