# input two series, output mutual_info and normalised mutual info
from sklearn import metrics
import multiprocessing as mp
from  multiprocessing import Pool
import time
import pandas as pd
from itertools import product, combinations
# entropy
def entropy(series):
      import scipy.stats as stats
      ser = series.value_counts/len(series)
      return(stats.entropy(ser))

def two_genes_mutual(p, mode,  *args):# within one chunk
    ser_one, ser_two= p

    if mode == 'one_chunk':
        chunk = args[0]

        orn = metrics.mutual_info_score(chunk[ser_one], chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], chunk[ser_two])
    if mode == 'two_chunk':
        chunk = args[0]
        other_chunk = args[1]
        orn = metrics.mutual_info_score(chunk[ser_one], other_chunk[ser_two])
        nrm = metrics.normalized_mutual_info_score(chunk[ser_one], other_chunk[ser_two])

    #outfile = kwargs['file']
    #with open(outfile, 'a') as f:
    #      f.write(ser_one +','+ ser_two+',' + str(orn)+',' + str(nrm) + '\n')

    return([ser_one, ser_two, str(orn)[:5], str(nrm)[:5]]) # to 3 digits is enough

def run_chunk(pairs,mode, *argv):
    if mode == 'one_chunk':
        chunk = argv[0]

        with Pool(15) as p:
            result = [p.apply_async(two_genes_mutual, args = (pp, mode, chunk)).get() for pp in pairs]

    if mode == 'two_chunk':
        chunk = argv[0]
        other_chunk = argv[1]
        with Pool(15) as p:
             result = [p.apply_async(two_genes_mutual, args = (pp, mode, chunk, other_chunk)).get() for pp in pairs]


    return(result)

def write_chunk(result, outfile):

    with open(outfile, 'a') as f:
        for r in result:
            f.write(','.join(r)+'\n')
