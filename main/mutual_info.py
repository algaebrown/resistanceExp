
# input: discretised pivot table, two kinds: quantile discretisation and fixed
in_path = '/home/hermuba/data0118/mutual_info/'
path = in_path + 'blastp_out_max_evalue_pivot.smpl_ordinary40'
outfile = path + '_mutual'

from Genome.context.mutual import *

t0 = time.time()
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
    t2 = time.time()
    # tell the function to work with only one chunk
    r = run_chunk(pairs, 'one_chunk', chunk)
    t3 = time.time()
    write_chunk(r, outfile)
    t4 = time.time()


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


            run_chunk(pairs, 'two_chunk', chunk, other_chunk)
            write_chunk(r, outfile)


            another_chunk_no += 1
    print(chunk_no, 'done')

    t5 = time.time()
    chunk_no += 1
