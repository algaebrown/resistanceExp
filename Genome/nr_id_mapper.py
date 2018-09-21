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
            t = 'PDB_ID'
        elif len(i) == 8:
            t = 'ID' # uniprot
        elif len(i) == 10:
            t = 'genbank' ###what to convert in uniprot??genbank protein id?
        elif len(i) == 11:
            t = 'P_REFSEQ_AC' # both refseq
        elif len(i) == 14:
            t = 'P_REFSEQ_AC' # both refseq
        if 'pir' in i:
            t = 'PIR' # protein info resource
        if 'prf' in i:
            t = 'prf' # prf|accession|name
        #else:
        #    print(i)
        return(t)

    df['id_type'] = df['sseqid'].map(id_mapper)


    return(df)
d = nr_to_uniprot_id(dmnd)

# refseq does not need modify

# PDB
for index in d.loc[d['id_type'] == 'PDB_ID'].index:
    pdb_id = d.loc[index, 'sseqid'][:4]
    d.loc[index, 'query_id'] = pdb_id
    print(pdb_id)



for index in d.loc[d['id_type'] == 'ID'].index:
    uniprot_id = d.loc[index, 'sseqid'][:-2]
    d.loc[index, 'query_id'] = uniprot_id
    print(uniprot_id)

# need no change
no_change = ['P_REFSEQ_AC', 'PIR']
for index in d.loc[d['id_type'].isin(no_change)].index:
    d.loc[index, 'query_id'] = d.loc[index, 'sseqid']


# genbank and prf: don't know how to use id mapper, probably by search
