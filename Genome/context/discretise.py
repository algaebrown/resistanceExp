# input: pivot table
in_path = '/home/hermuba/data0118/mutual_info/'
table_name = 'blastp_max_e_value'

in_file = in_path + table_name + '_pivot'
quantile = in_file + table_name + '_quantile'
ordinary = in_file + table_name + '_ordinary'

import pandas as pd
# fillna, discretise using two methods:
def discrete(df):
    df.fillna(inplace = True)

    q_table = pd.DataFrame(index = df.index, columns = df.columns)
    c_table = pd.DataFrame(index = df.index, columns = df.columns)

    for i for df.index:
        q_table.loc[i] = pd.qcut(df.loc[i], 415)
        c_table.loc[i] = pd.ccut(df.loc[i], 415)

    return(q_table, c_table)







chunks = pd.read_csv(in_file, header = 0, index_col = 0, chunksize = 5, iterator = True)
no_chunk = 0
for chunk in chunks:
    q, c = discrete(chunk)

    with open(quantile) as f:

        if no_chunk == 0:
            q.to_csv(f, header = True)

        else:
            q.to_csv(f, header = False)
    with open(ordinary) as f:
        if no_chunk == 0:
            c.to_csv(f, header = True)

        else:
            c.to_csv(f, header = False)
    no_chunk += 1
