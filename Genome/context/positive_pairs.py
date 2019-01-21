filename = '/home/hermuba/data0118/mutual_info/blastp_out_max_evalue_pivot_ordinary40_mutual'
import pandas as pd

for chunk in pd.read_csv(filename, chunksize=10**4, names = ['gene_one', 'gene_two', 'mutual_info', 'nrm_mutual'], header = 0):
        select = chunk.loc[chunk['nrm_mutual']>0.658]
            with open('/home/hermuba/data0118/network1122/refseq_ordinary_40', 'a') as f:
                        select.to_csv(f, header = False)
                                print(select.shape)
