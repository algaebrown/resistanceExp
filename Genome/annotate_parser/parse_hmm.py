infile = '/home/hermuba/data0118/EC70_resfam.tab'

import pandas as pd

def parse_hmm(infile):
    '''
    to parse hmmsearch -tblout, originally designed to resfam.hmm offered by dantas lab
    input: file
    output: dataframe
    '''

    df = pd.read_csv(infile, sep=r"\s*", names = ['target name', 'target_acc', 'query name', 'query_acc', 'full-evalue', 'full-score', 'full-bias','domain-evalue', 'domain-score', 'domain-bias'], usecols = [0,1,2,3,4,5,6,7,8,9], na_values = '-', comment = '#')

    return(df)
