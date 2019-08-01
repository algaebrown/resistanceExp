# this is a script to parse interpro output ran with the shell script at ~/resistanceExp/Genome/run_interproscan.sh

# header
import pandas as pd
def parse(infile):
    h = ['qseqid', 'seq_md5', 'len', 'analysis', 'accession', 'description', 'start', 'end', 'evalue', 'status', 'date', 'ipr_accession', 'ipr_describe', 'goterm', 'pathway']

    # read tsv

    df = pd.read_csv(infile, names = h, sep = '\t', na_values = 'NaN')

    return(df)

def extract_term(df, anno):
    '''
    extract goterm for one qseqid
    return series with qseqid and set of goterms

    input: df = interpro dataframe; anno = 'goterm';'pathway','accession', 'ipr_accession'
    '''


    # drop those without goterm
    no_na_df = df.dropna(axis = 'index', subset = [anno])

    # groupby and combin goterm for a specific qseqid
    go_term_sum = no_na_df.groupby(by = 'qseqid')[anno].apply(lambda x: "%s" % '|'.join(x))

    # to remove redundant go terms from concatenation
    no_redun_go = go_term_sum.apply(lambda x: set(x.split('|')))

    return(no_redun_go)


def extract_card(card_df):
    '''
    input: card dataframe with rows = representing gene; column = ARO
    output: series with index = representing gene; value = set of ARO
    '''
    card_s = pd.Series(index = card_df.index)
    for index, row in card_df.iterrows():
        card_s.loc[index] = set(row.loc[row == 1].index)
    return(card_s)
