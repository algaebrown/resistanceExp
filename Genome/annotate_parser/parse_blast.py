import pandas as pd
def parse_blast(blast_file):
    """
    To parse blastp nr output to dataframe
    input: blastp --in qseqid, sseqid, evalue, bitscore, sgi, sacc, staxods, stitle; TAB-delimited
    output: dataframe
    """
    df = pd.read_csv(blast_file, names = ['qseqid', 'sseqid', 'evalue', 'bitscore', 'sgi', 'sacc', 'staxids', 'stitle'], delimiter = '\t')
    return(df)

def parse_diamond(dmnd_file):
    '''
    parsing data output from diamond blastp nr
    input: file from Genome/run/dmnd_nr.sh; storing in data0118/cdhit/dmnd_nr;
    output: dataframe
    '''
    df = pd.read_csv(dmnd_file, names = ['qseqid','qlen', 'sseqid','slen','sstart', 'send', 'qstart', 'qend', 'evalue', 'bitscore', 'stitle'], delimiter = '\t')

    return(df)

def aclame_preprocess(df):
    # remove bad evalue
    df = df.loc[df['evalue']<0.00001]

    return(df)
