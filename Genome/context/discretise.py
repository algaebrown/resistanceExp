# input: pivot table
in_path = '/home/hermuba/data0118/mutual_info/'
table_name = 'eskape_blastp_out_max_evalue'

in_file = in_path + table_name + '_pivot'
#quantile = in_path + table_name + '_quantile'
ordinary = in_path + table_name + '_ordinary_label'

import pandas as pd
from  multiprocessing import Pool


# fillna, discretise using two methods:
def discrete(df):
    df.fillna(0, inplace = True)

    #q_table = pd.DataFrame(index = df.index, columns = df.columns)
    c_table = pd.DataFrame(index = df.index, columns = df.columns)

    for index, rows in df.iterrows():
        c_table.loc[rows.name] = pd.cut(rows, 415, labels = False)



    return(c_table)







chunks = pd.read_csv(in_file, header = 0, index_col = 0, chunksize = 100, iterator = True)
no_chunk = 0
for chunk in chunks:
    c = discrete(chunk)


    if no_chunk == 0:

       # with open(quantile, 'w') as f:
       #     q.to_csv(f, header = True)
        with open(ordinary, 'w') as f:
            c.to_csv(f, header = True)
    else:
        #with open(quantile, 'a') as f:
        #    q.to_csv(f, header = False)
        with open(ordinary, 'a') as f:
            c.to_csv(f, header = False)
    no_chunk += 1