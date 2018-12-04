blast_file = '/home/hermuba/data0118/Ecoli70Blast_e10-5tar1'

import pandas as pd
def parse_blast(blast_file):
    df = pd.read_csv(blast_file, names = ['qseqid', 'sseqid', 'evalue', 'bitscore', 'sgi', 'sacc', 'staxids', 'stitle'], delimiter = '\t')
    df.to_pickle('/home/hermuba/data0118/ec_test_tar1')

def parse_diamond(dmnd_file):
    df = pd.read_csv(dmnd_file, names = ['qseqid', 'sseqid', 'evalue', 'bitscore', 'staxids', 'stitle', 'sseq'], delimiter = '\t')
    # --outfmt qseqid sseqid evalue bitscore staxids stitle sseq
    return(df)
