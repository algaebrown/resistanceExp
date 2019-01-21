
# this is a script to parse interpro output ran with the shell script at ~/resistanceExp/Genome/run_interproscan.sh

# input file
infile = '/home/hermuba/data0118/interpro/ec70_20180929'
outfile = '/home/hermuba/data0118/goldstandard/tf_intersect_rm_GO'

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

#out_df = pd.DataFrame()

def extract_card(card_df):
    '''
    input: card dataframe with rows = representing gene; column = ARO
    output: series with index = representing gene; value = set of ARO
    '''
    card_s = pd.Series(index = card_df.index)
    for index, row in card_df.iterrows():
        card_s.loc[index] = set(row.loc[row == 1].index)
    return(card_s)

def link_or_not(go_set1, go_set2):



    inter = go_set1.intersection(go_set2)
    if 'GO:0003677' in inter:
        inter.remove('GO:0003677')

    if len(inter) > 0:
        answer = 1
    else:
        answer = 0


    return(answer)
    #out_df = out_df.append([[name1, name2, answer]])
    #print(out_df.shape)

def gold_standard(anno_df, term, outfile):

    # write header
    outfile = outfile + term
    with open(outfile, 'w') as f:
        f.write('gene_one,gene_two,goldstandard\n')

    s = anno_df[term].dropna() # remove nan
    import itertools

    all_pairs = itertools.combinations(s.index, 2)

    #print(len(all_pairs))

    # multiprocess
    #arg_lists = [[no_redun_go[p[0]], no_redun_go[p[1]], p[0], p[1]] for p in all_pairs]
    #print('done arg lists')

    #from multiprocessing import Pool
    #with Pool(8) as p:
    #    p.map(link_or_not, arg_lists)
    itxn = []
    n1 = []
    n2 = []
    for p in all_pairs:
        l = link_or_not(s[p[0]], s[p[1]])
        itxn.append(l)
        n1.append(p[0])
        n2.append(p[1])

        with open(outfile, 'a') as f:
            f.write(','.join([p[0], p[1], str(l)])+'\n')
    #return(n1, n2, itxn)

# execute
#df = parse(infile)
#no = extract_goterm(df)
#gold_standard(no)
