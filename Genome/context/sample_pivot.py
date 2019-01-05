# to create a subset of pivot table from sampled benchmarking
import pandas as pd
def sampled_pivot(original_pivot, sampled, outfile):

    # read original pivot table in chunk
    chunks = pd.read_csv(original_pivot, header = 0, index_col = 0, chunksize = 100, iterator = True)
    no_chunk = 0
    # import sampled, gene name in index
    s = pd.read_pickle(sampled)

    # iterate through it
    for chunk in chunks:
        print('running chunk ', no_chunk)

        subset = chunk.loc[chunk.index.isin(s.index.str.replace('.', '').str.replace('|', ''))] ##### temporary as id replacement is slowwwwww

        if no_chunk == 0:
            with open(outfile, 'w') as f:
                subset.to_csv(f, header = True)
                no_chunk +=1

        else:
            with open(outfile, 'a') as f:
                subset.to_csv(f, header = False)
                no_chunk += 1
original_pivot = '/home/hermuba/data0118/mutual_info/blastp_out_max_evalue_pivot'

sampled = '/home/hermuba/data0118/bench_set/sampled_gold_200'
outfile = '/home/hermuba/data0118/mutual_info/blastp_out_max_evalue_pivot.smpl'
