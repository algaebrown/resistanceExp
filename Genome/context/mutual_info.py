# input: discretised pivot table, two kinds: quantile discretisation and fixed
in_path = '/home/hermuba/data0118/mutual_info/'
table_name = 'eskape_blastp_out_max_evalue'

quantile = in_path + table_name + '_quantile'
ordinary = in_path + table_name + '_ordinary_label'

path = ordinary
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
    t1 = time.time()
    if mode == 'one_chunk':
        orn = metrics.mutual_info_score(chunk[ser_one], chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], chunk[ser_two])
    if mode == 'two_chunk':
        orn = metrics.mutual_info_score(chunk[ser_one], other_chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], other_chunk[ser_two])
    t2 = time.time()
    #print("calculate", t2-t1)

    with open(outfile, 'a') as f:
          f.write(ser_one +','+ ser_two+',' + str(orn)+',' + str(nrm) + '\n')

# main


chunk_iter1 = pd.read_csv(path, chunksize = 50, header = 0, index_col = 0)
chunk_no = 0

# write header to csv
with open(outfile, 'w') as f:
    f.write('gene_one,gene_two,mutual_info,nrm_mutual\n')

for chunk in chunk_iter1:
    t0 = time.time()

    # tranpose uses even more memory, and when they dbecome series, there is no difference. However, tranpose allow faster mutual info calculation (10 times faster)
    chunk.transpose(copy = False)
    chunk.dropna(axis = 'index', inplace = True)



    # all combinations of a chunk
    pairs = list(combinations(chunk.columns, 2))


    t1 = time.time()
    print(t1-t0, 'read 1 chunk')

    # tell the function to work with only one chunk
    mode = 'one_chunk'
    with Pool(15) as p:

        print(p.map(two_genes_mutual, pairs))

    t4 = time.time()
    print(t4-t1, 'map a chunk')

    # save all results to file

    t5 = time.time()
    print(t5-t4, 'write a chunk')
    print((t5-t0), 'for one chunk')


    # with other chunks
    chunk_iter2 = pd.read_csv(path, chunksize = 50, header = 0, index_col = 0)
    another_chunk_no = 0
    for other_chunk in chunk_iter2:

        if another_chunk_no <= chunk_no: # means we have calcuated before
            another_chunk_no += 1
        else:
            # clean data
            other_chunk.transpose(copy = False)
            other_chunk.dropna(axis = 'columns', inplace = True)

            # a new df to save


            # pairs
            pairs = list(product(chunk.columns, other_chunk.columns))


            mode = 'two_chunk'
            with Pool(15) as p:
                p.map(two_genes_mutual, pairs)


            another_chunk_no += 1

    chunk_no += 1
chunk_by(ordinary)
