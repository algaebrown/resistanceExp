# input: file from diamond blastp, already converted to dataframe
import pandas as pd
dmnd = pd.read_pickle("/home/hermuba/data0118/ecoli70_dmnd_df")

# output: the dataframe added with uniprot id
out_path = "/home/hermuba/data0118/ecoli70_dmnd_df_uniprot"

'''
goal: becuase the ssequid from nr database is a mixture of pdb id, genbank id ......etc, we need a script to sift out each kind of id, send them to uniprot id converter, and get a list of uniprot id (to feed into the EVEX database)
'''

def nr_to_uniprot_id(df):

    # identify types of id

    def id_mapper(i):
        if len(i) == 6:
            t = 'pdb'
        if len(i) == 8:
            t = 'uniprot'
        if len(i) == 10:
            t = 'genbank'
        if len(i) == 11:
            t = 'refseq'
        if len(i) == 14:
            t = 'refseq'
        if 'pir' in i:
            t = 'uniparc'
        return(t21)

    df['id_type'] = df['sseqid'].map(id_mapper)

    # modify some kinds of id
    df['new_id'] = df['sseqid']
    df.loc[df['id_type']=='pdb']['new_id'] = df.loc[df['id_type']=='pdb']['sseqid'].str[:-2] # ex: 2WCI_A to 2WCI

    return(df)
