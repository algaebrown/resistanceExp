
# input: discretised pivot table, two kinds: quantile discretisation and fixed
in_path = '/home/hermuba/data0118/mutual_info/'
table_name = 'blastp_out_max_evalue_pivot_ordinary40'

path = in_path + table_name
outfile = path + '_mutual'

# input two series, output mutual_info and normalised mutual info
from sklearn import metrics

from  multiprocessing import Pool
import time
import pandas as pd
from itertools import product, combinations

# entropy
def entropy(series):
      import scipy.stats as stats
      ser = series.value_counts/len(series)
      return(stats.entropy(ser))

def two_genes_mutual(args):# within one chunk
    ser_one, ser_two= args
    global mode
    global save
    global chunk
    global other_chunk

    if mode == 'one_chunk':
        orn = metrics.mutual_info_score(chunk[ser_one], chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], chunk[ser_two])
    if mode == 'two_chunk':
        orn = metrics.mutual_info_score(chunk[ser_one], other_chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], other_chunk[ser_two])


    with open(outfile, 'a') as f:
          f.write(ser_one +','+ ser_two+',' + str(orn)+',' + str(nrm) + '\n')
    #save = save + ser_one +','+ ser_two+',' + str(orn)+',' + str(nrm) + '\n'

# main
chunk_iter1 = pd.read_csv(path, chunksize = 50, header = 0, index_col = 0)
chunk_no = 0
t1 = time.time()
# write header to csv
with open(outfile, 'w') as f:
    f.write('gene_one,gene_two,mutual_info,nrm_mutual\n')

for chunk in chunk_iter1:
    print('this is chunk ' , chunk_no)


    # tranpose uses even more memory, and when they dbecome series, there is no difference. However, tranpose allow faster mutual info calculation (10 times faster)
    chunk = chunk.transpose(copy = False)
    chunk.dropna(axis = 'index', inplace = True)

    # all combinations of a chunk
    pairs = list(combinations(chunk.columns, 2))

    # tell the function to work with only one chunk
    mode = 'one_chunk'
    with Pool(15) as p:
        p.map(two_genes_mutual, pairs)

    # with other chunks
    chunk_iter2 = pd.read_csv(path, chunksize = 50, header = 0, index_col = 0)
    another_chunk_no = 0

    for other_chunk in chunk_iter2:

        if another_chunk_no <= chunk_no: # means we have calcuated before
            another_chunk_no += 1
        else:
            # clean data
            print(chunk_no, another_chunk_no, 'processing')
            other_chunk = other_chunk.transpose(copy = False)
            other_chunk.dropna(axis = 'columns', inplace = True)

            # pairs
            pairs = list(product(chunk.columns, other_chunk.columns))

            mode = 'two_chunk'
            with Pool(15) as p:
                p.map(two_genes_mutual, pairs)


            another_chunk_no += 1
    print(chunk_no, 'done')
    t2 = time.time()
    print(t2-t1)
    chunk_no += 1
