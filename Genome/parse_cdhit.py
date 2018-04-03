# readfile

cdhit_result = '../../data/genePredicted/cdhit/ec0913.clstr'

f = open(cdhit_result)

# create dataframe
import pandas as pd
df = pd.DataFrame()
cluster_detail = pd.DataFrame(columns = ['representing gene length', 'representing gene header', 'mean similarity', 'mean length', 'member'])


for line in f:
    if line[0] == '>':
        columnName = line.rstrip()[1:]
        sim_sum = 0
        len_sum = 0
        member = ''
    else:
        isrepresent = line[-2]
        ID = line.split('|')[1].split('...')[0]
        number = int(line.split('\t')[0])+1


        gene_name = line.split('|')[0].split('>')[1]
        length = int(line.split('\t')[1].split('aa')[0])
        df.loc[ID, columnName] = True

        # save member
        member = member + ',' + gene_name + '|' + ID
        cluster_detail.loc[columnName, 'member'] = member

        if isrepresent == '*':
            cluster_detail.loc[columnName, 'representing gene length'] = length
            cluster_detail.loc[columnName, 'representing gene header'] = gene_name + '|'+ ID
            print(gene_name)
        else:

            identity = float(line.split('at ')[1].replace('%', ''))
            sim_sum = sim_sum + identity
            len_sum = len_sum + length

            cluster_detail.loc[columnName, 'mean similarity'] = sim_sum / number
            cluster_detail.loc[columnName, 'mean length'] = length / number


df = df.fillna(False)
df.to_pickle("../../data/genePredicted/cdhit/ec0913_df")
cluster_detail.to_pickle("../../data/genePredicted/cdhit/cluster_detail_df")
f.close()
