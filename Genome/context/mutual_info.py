
# input: discretised pivot table, two kinds: quantile discretisation and fixed
in_path = '/home/hermuba/data0118/mutual_info/'
table_name = 'eskape_blastp_out_max_evalue_pivot_new_ordinary40'

path = in_path + table_name

#

outfile = path + '_mutual'
checkpoint_file = outfile + '.checkpoint'

# input two series, output mutual_info and normalised mutual info
from sklearn import metrics
import pickle
from  multiprocessing import Pool
import time
import pandas as pd
from itertools import product, combinations

# checkpointing
def create_checkpoint(chunk_no, another_chunk_no, checkpoint_file):
    ckp = dict()
    ckp['chunk_no'] = chunk_no
    ckp['another_chunk_no'] = another_chunk_no
    with open(checkpoint_file, 'wb') as f:
          pickle.dump(ckp, f)

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
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], chunk[ser_two], average_method = 'geometric')
    if mode == 'two_chunk':
        orn = metrics.mutual_info_score(chunk[ser_one], other_chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], other_chunk[ser_two], average_method = 'geometric')


    with open(outfile, 'a') as f:
          f.write(ser_one +','+ ser_two+',' + str(orn)+',' + str(nrm) + '\n')
    #save = save + ser_one +','+ ser_two+',' + str(orn)+',' + str(nrm) + '\n'

# main
chunk_iter1 = pd.read_csv(path, chunksize = 50, header = 0, index_col = 0)


# If previous checkpoint does not exist
import os
if os.path.isfile(checkpoint_file) == False:
      print("no checkpoint exist")
      # start from scratch
      chunk_no = 0

      cpk_chunk_no = 0
      cpk_another_chunk_no = -1

      # write header to new csv file
      with open(outfile, 'w') as f:
            f.write('gene_one,gene_two,mutual_info,nrm_mutual\n')

else:
      # restore to previous point
      with open(checkpoint_file, 'rb') as f:
            cpk = pickle.load(f)
            cpk_chunk_no = cpk['chunk_no']
            cpk_another_chunk_no = cpk['another_chunk_no']

print("file status: ", str(cpk_chunk_no), str(cpk_another_chunk_no))

for chunk in chunk_iter1:




    if cpk_chunk_no > 0: # need to skip some
          chunk_no = cpk_chunk_no

          for i in range(cpk_chunk_no):
                chunk = next(chunk_iter1)
                print("skipping ",str(i))
          cpk_chunk_no = -1

    create_checkpoint(chunk_no, -1, checkpoint_file)
    # tranpose uses even more memory, and when they dbecome series, there is no difference. However, tranpose allow faster mutual info calculation (10 times faster)
    chunk = chunk.transpose(copy = False)
    chunk.dropna(axis = 'index', inplace = True)



    # check if "another chunk" has already started"; if not, do within the chunk
    if cpk_another_chunk_no == -1: # not started yet
          print("starting ", str(chunk_no))

          # all combinations of a chunk
          pairs = list(combinations(chunk.columns, 2))

          # tell the function to work with only one chunk
          mode = 'one_chunk'
          with Pool(15) as p:
                p.map(two_genes_mutual, pairs)
          # initiate
          another_chunk_no = 0

    # with other chunks
    chunk_iter2 = pd.read_csv(path, chunksize = 50, header = 0, index_col = 0)

    for other_chunk in chunk_iter2:
          # skipping some if already done
          if cpk_another_chunk_no > 0: # started from midpoint
                another_chunk_no = cpk_another_chunk_no

                for i in range(cpk_another_chunk_no):
                      other_chunk = next(chunk_iter2)
                      print("skipping ", str(i))
                cpk_another_chunk_no = -1 # only use once

          # check if this is necessary
          if another_chunk_no <= chunk_no: # means we have calcuated before
            another_chunk_no += 1
          else:
            # clean data
            print(chunk_no, another_chunk_no, 'processing')
            create_checkpoint(chunk_no, another_chunk_no, checkpoint_file)

            other_chunk = other_chunk.transpose(copy = False)
            other_chunk.dropna(axis = 'columns', inplace = True)

            # pairs
            pairs = list(product(chunk.columns, other_chunk.columns))

            mode = 'two_chunk'
            with Pool(15) as p:
                p.map(two_genes_mutual, pairs)


            another_chunk_no += 1

    print(chunk_no, 'done')


    chunk_no += 1

# in the end, delete checkpoint file
import os
os.remove(checkpoint_file)
