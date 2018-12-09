

#table_name = 'blastp_out_max_evalue'
#in_file = in_path + table_name + '_pivot'



import pandas as pd
from  multiprocessing import Pool


# fillna, discretise using two methods:
def ordinary(df, dataset):
    df.fillna(0, inplace = True)
    c_table = pd.DataFrame(index = df.index, columns = df.columns)
    for index, rows in df.iterrows():
        c_table.loc[rows.name] = pd.cut(rows, 415, labels = False)
    return(c_table)


def quantile(df, dataset):
    import numpy as np
    bin_path = '/home/hermuba/data0118/discretize/'
    if dataset == 'eskape':
        npy = 'eskape_bins.npy'
    if dataset == 'refseq':
        npy = 'refseq_bins.npy'

    npy = bin_path + npy

    precalculated_bin = np.load(npy)
    precalculated_bin = np.append(precalculated_bin, 1.1) # add right boarder to make sure 1 will be captured





    q_table = pd.DataFrame(index = df.index, columns = df.columns)

    for index, rows in df.iterrows():
        q_table.loc[rows.name] = pd.cut(rows, precalculated_bin, labels = list(range(1, len(precalculated_bin))))

    return(q_table.fillna(0))



def run_chunkwise(in_file, discrete_method, dataset):
    '''
    Taking transformed e-value table as the input; discretize using two methods
    input:
    1. in_file:pivot table at '/home/hermuba/data0118/mutual_info/'
    2. discrete_method: `ordinary` or `quantile``
    3. dataset: 'refseq' or 'eskape'; when using discrete_equal_bulk, require different precalculated binning.
    output: file in same path, add _quantile or _ordinary
    '''
    in_path = '/home/hermuba/data0118/mutual_info/'

    # read file as chunk (chunksize = 100)
    chunks = pd.read_csv(in_file, header = 0, index_col = 0, chunksize = 100, iterator = True)
    no_chunk = 0

    # run discretise for each chunk
    for chunk in chunks:
        print('running chunk ',no_chunk)
        c = discrete_method(chunk, dataset)

        # write to file chunkwise
        outfile = in_path + table_name + discrete_method.__name__

        # add header to first line
        if no_chunk == 0:

            with open(outfile, 'w') as f:
                c.to_csv(f, header = True)
        # if not first chunk, no need to add header
        else:
            with open(outfile, 'a') as f:
                c.to_csv(f, header = False)
        no_chunk += 1

##### remember to rerun 'discrete'
