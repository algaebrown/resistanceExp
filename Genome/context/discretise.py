# input: pivot table
in_path = '/home/hermuba/data0118/mutual_info/'
table_name = 'eskape_blastp_out_max_evalue'

in_file = in_path + table_name + '_pivot'
quantile = in_path + table_name + '_quantile'
ordinary = in_path + table_name + '_ordinary'

import pandas as pd
from  multiprocessing import Pool


# fillna, discretise using two methods:
def discrete(df):
    df.fillna(0, inplace = True)

    #q_table = pd.DataFrame(index = df.index, columns = df.columns)
    c_table = pd.DataFrame(index = df.index, columns = df.columns)

    for index, rows in df.iterrows():
        # how many slice should Inuse
        # hshould we normalise on all genes or for one gene?
        c_table.loc[rows.name] = pd.cut(rows, 415, labels = False)
        #q_table.loc[rows.name] = pd.qcut(rows, 40, labels = False)


    #return(c_table, q_table)
    return(c_table)


def discrete_equal_bulk(npy, df):
    import numpy as np
    precalculated_bin = np.load(npy)

    q_table = pd.DataFrame(index = df.index, columns = df.columns)

    for index, rows in df.iterrows():
        q_table.loc[rows.name] = pd.cut(rows, precalculated_bin)

    return(q_table.fillna(0))



chunks = pd.read_csv(in_file, header = 0, index_col = 0, chunksize = 100, iterator = True)
no_chunk = 0
for chunk in chunks:
    c = discrete(chunk)


    if no_chunk == 0:

        #with open(quantile, 'w') as f:
            #q.to_csv(f, header = True)
        with open(ordinary, 'w') as f:
            c.to_csv(f, header = True)
    else:
        #with open(quantile, 'a') as f:
            #q.to_csv(f, header = False)
        with open(ordinary, 'a') as f:
            c.to_csv(f, header = False)
    no_chunk += 1
