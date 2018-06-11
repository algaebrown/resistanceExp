blast_file = '/home/hermuba/data0118/Ecoli70Blast_e10-5tar1'

import pandas as pd
df = pd.read_csv(blast_file, names = ['qseqid', 'sseqid', 'evalue', 'bitscore', 'sgi', 'sacc', 'staxids', 'stitle'], delimiter = '\t')
df.to_pickle('/home/hermuba/data0118/ec_test_tar1')
