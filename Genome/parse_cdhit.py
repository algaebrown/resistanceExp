# readfile
cdhit_path = '../../data/genePredicted/cdhit/'


import pandas as pd

# a function to convert .clstr file from CD-hit to
# output 1: absense/presence pattern in pandas dataframe format
# output 2: _cluster_detail file containing basic info of each cluster
def clstr_to_df(filename):

    f = open(cdhit_path + filename)

    # create dataframe

    df = pd.DataFrame()
    cluster_detail = pd.DataFrame(columns = ['representing gene length', 'representing gene header', 'mean similarity', 'mean length', 'member'])


    for line in f:

        if line[0] == '>':


            columnName = line.rstrip()[1:]
            print("doing cluster ", columnName)
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
    df.to_pickle(cdhit_path+filename+"_df")
    cluster_detail.to_pickle(cdhit_path+filename+"cluster_detail")
    f.close()

f_name = ['ec90.clstr', 'ec80.clstr', 'ec70.clstr']
for f in f_name:
    clstr_to_df(f)
    print(f, "done")
