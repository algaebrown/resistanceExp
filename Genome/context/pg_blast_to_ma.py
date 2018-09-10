# input: postgresql blastp_out_max_evalbue table, with qseqid, evalue, target genome
# output:
import pandas as pd
import psycopg2
from Genome.context.config import config

outfile = '/home/hermuba/data0118/mutual_info/20180903'

params = config()
#params['database'] = 'hermuba' ##test

table_name = 'blastp_abs'
in_table = 'blastp_out_max_evalue'
#in_table = 'test_max_evalue' ###test

conn = psycopg2.connect(**params)
cur = conn.cursor()

# get list of protein of interest
print("getting protein list")
cur.execute("""
SELECT DISTINCT qseqid

FROM {0}
""".format(in_table))
protein_list = [i[0] for i in cur.fetchall()]

# get list of target genome
print("getting target genome list")
cur.execute("""
SELECT DISTINCT target_genome
FROM {0}

""".format(in_table))

target_g_list = [i[0] for i in cur.fetchall()]

# extract pivot table from DB
def two_genes(gene_one, gene_two):
    def add_quote(gene):
        return('\'' + gene + '\'')

    row_string = '\"' + gene_one + '\"'+ 'decimal,' + '\"'+ gene_two +'\"'+ 'decimal'
    cur.execute("""
    select * from crosstab($$select target_genome,qseqid,trans_evalue from {0}
    where qseqid = {1} or qseqid = {2}$$)
    as t(target_genome text, {3})

    """.format(in_table, add_quote(gene_one), add_quote(gene_two), row_string))
    x = cur.fetchall()

    # trasnform into dataframe
    df = pd.DataFrame(index = target_g_list, columns = [gene_one, gene_two])
    for t_genome in x:
        def zero_or_value(e):
            if e == None:
                return(0)
            else:
                return(float(e))
        df.loc[t_genome[0]] = [zero_or_value(t_genome[1]), zero_or_value(t_genome[2])]
    df.fillna(0, inplace = True)



    return(df)






import itertools
from sklearn import metrics
from multiprocessing import Pool

# calculate entropy from a series containing normalised discretised e-value
def entropy(series):
      import scipy.stats as stats
      ser = series.value_counts/len(series)
      return(stats.entropy(ser))

# discretise a pair of e-value series and calculcate mutual information, then write to file
def two_mutual(combination):

    gene_one = combination[0]
    gene_two = combination[1]



    # fetch pivot table of the two genes
    df = two_genes(gene_one, gene_two)
    print('calulating: ', gene_one, gene_two, df.shape())
    # quantile distribution + ordinary mutual information
    try:
        df['q_discrete_one'] = pd.qcut(df[gene_one], 415)
        df['q_discrete_two'] = pd.qcut(df[gene_two], 415)
        q_mutual_info = metrics.mutual_info_score(df['q_discrete_one'], df['q_discrete_two'])
    except ValueError:
        print("no quantile discretisation, grant mutual info na")
        q_mutual_info = 'na'

    # ordinary distribution + mutual information + save entropy for each
    df['discrete_one'] = pd.cut(df[gene_one], 415)
    df['discrete_two'] = pd.cut(df[gene_two], 415)
    i_mutual_info = metrics.mutual_info_score(df['discrete_one'], df['discrete_two'])
    i_norm_mutual_info = metrics.normalized_mutual_info_score(df['discrete_one'], df['discrete_two'])
    entropy_one = entropy(df['discrete_one'])
    entropy_two = entropy(df['discrete_two'])


    # write to file
    with open(outfile, 'a') as f:
        print("write to file ", outfile)
        f.write(gene_one + '\t' +   gene_two + '\t' +  q_mutual_info + '\t'+ i_mutual_info + '\t'+ i_norm_mutual_info + '\t' +  entropy_one + '\t' + entropy_two + '\n')


# execute with multiprocessing
with Pool(12) as p:
    print(p.map(two_mutual, list(itertools.combinations(protein_list, 2))))

cur.close()
conn.close()
