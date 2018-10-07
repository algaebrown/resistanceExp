# this is a script to parse interpro output ran with the shell script at ~/resistanceExp/Genome/run_interproscan.sh

# input file
infile = '/home/hermuba/data0118/interpro/ec70_20180929'
outfile = '/home/hermuba/data0118/goldstandard/tf_intersect'

# header
import pandas as pd
def parse(infile):
    h = ['qseqid', 'seq_md5', 'len', 'analysis', 'accession', 'description', 'start', 'end', 'evalue', 'status', 'date', 'ipr_accession', 'ipr_describe', 'goterm', 'pathway']

    # read tsv

    df = pd.read_csv(infile, names = h, sep = '\t', na_values = 'NaN')

    return(df)


def extract_goterm(df):
    '''
    extract goterm for one qseqid
    return series with qseqid and set of goterms
    '''


    # drop those without goterm
    no_na_df = df.dropna(axis = 'index', subset = ['goterm'])

    # groupby and combin goterm for a specific qseqid
    go_term_sum = no_na_df.groupby(by = 'qseqid')['goterm'].apply(lambda x: "%s" % '|'.join(x))

    # to remove redundant go terms from concatenation
    no_redun_go = go_term_sum.apply(lambda x: set(x.split('|')))

    return(no_redun_go)

#out_df = pd.DataFrame()

def link_or_not(args):

    go_set1, go_set2, name1, name2 = args

    inter = go_set1.intersection(go_set2)
    #print(type(inter))
    if len(inter) > 0:
        answer = 1
    else:
        answer = 0

    with open(outfile, 'a') as f:
        f.write(name1 + ',' + name2 + ',' + str(answer) + '\n')
    #out_df = out_df.append([[name1, name2, answer]])
    #print(out_df.shape)

def gold_standard(no_redun_go):

    # write header
    with open(outfile, 'w') as f:
        f.write('gene1,gene2,answer\1n')


    import itertools
    all_pairs = itertools.combinations(no_redun_go.index, 2)
    #print(len(all_pairs))

    # multiprocess
    #arg_lists = [[no_redun_go[p[0]], no_redun_go[p[1]], p[0], p[1]] for p in all_pairs]
    #print('done arg lists')

    #from multiprocessing import Pool
    #with Pool(8) as p:
    #    p.map(link_or_not, arg_lists)

    for p in all_pairs:
        link_or_not([no_redun_go[p[0]], no_redun_go[p[1]], p[0], p[1]])
# execute
df = parse(infile)
no = extract_goterm(df)
gold_standard(no)
