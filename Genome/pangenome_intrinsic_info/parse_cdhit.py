# readfile
# cdhit_path = '../../data/genePredicted/cdhit/'


import pandas as pd

# a function to convert .clstr file from CD-hit to
# input: filename: where is the .clstr; out_path: where is the df stored
# output 1: absense/presence pattern in pandas dataframe format
# output 2: _cluster_detail file containing basic info of each cluster
def clstr_to_df(filename,dfpath, detailpath):
    """
    clstr_to_df turns .clstr file generated from CD-HIT to dataframes. One dataframe is absence-presence parttern, which will be stored under the path `dfpath`. The other is some details (similarity, length, gene header......etc) which will be saved in `detailpath`.

    input:
    1. filename: .clstr file
    2. dfpath: the folder to store absence-presence dataframe
    3. detail path: the folder to store cluster_detail dataframe
    the name of output dataframe will be FILENAME_df and FILENAME_cluster_detail

    """
    with open(filename) as f:
        x = f.readlines()
    # create dataframe

    df = pd.DataFrame()
    cluster_detail = pd.DataFrame(columns = ['representing gene length', 'representing gene header', 'mean similarity', 'mean length', 'member'])


    for line in x:

        if line[0] == '>':

            columnName = line.rstrip()[1:]
            print(columnName)
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

            else:

                identity = float(line.split('at ')[1].replace('%', ''))
                sim_sum = sim_sum + identity
                len_sum = len_sum + length

                cluster_detail.loc[columnName, 'mean similarity'] = sim_sum / number
                cluster_detail.loc[columnName, 'mean length'] = length / number

    f_name = filename.split('/')[-1]
    df = df.fillna(False)
    df.to_pickle(dfpath+f_name+'df')
    cluster_detail.to_pickle(detailpath+f_name+'df')
    f.close()

# a function with one input:
from multiprocessing import Pool

import os
def folder_parse(folder):
    # to parse all .clstr in `folder`
    def one_input(f):
        dfpath = folder + 'pangenome_df/'
        detailpath = folder + 'cluster_detail/'
        print(f)
        return(clstr_to_df(folder + f, dfpath, detailpath))

    onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(folder+f)]


    p = Pool(5)
    print(p.map(one_input, onlyfiles))