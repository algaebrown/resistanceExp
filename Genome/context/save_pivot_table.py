import psycopg2
from Genome.context.config import config
params = config()
in_table = 'eskape_blastp_out_max_evalue'

base_path = '/home/hermuba/data0118/mutual_info/'+ in_table
pivot_table = base_path + '_pivot'
qcut = base_path + '_qcut'
cut = base_path + '_cut'

conn = psycopg2.connect(**params)
cur = conn.cursor()

# get list of protein of interest
print("getting protein list")
# index was added to table to speed up search


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


# add quote
def add_quote(gene):
    return('\'' + gene + '\'')

def zero_or_value(e):
    if e == None:
       return(0)
    else:
       return(float(e))

# align
import pandas as pd
def one_gene(qseqid):

    df = pd.DataFrame(columns = target_g_list, index = [qseqid])

    cur.execute("""
    SELECT target_genome, trans_evalue from {0}
    WHERE qseqid = {1}
    """.format(in_table, add_quote(qseqid)))

    x = cur.fetchall()

    for t_genome in x:
        if t_genome[0] in target_g_list:
            df.loc[qseqid, t_genome[0]] = float(zero_or_value(t_genome[1]))
        else:
            print(t_genome[0])


    return(df)

# write to file
def write_to(qseqid):
    d = one_gene(qseqid)
    with open(pivot_table,'a') as f:
        d.to_csv(f, header = False, float_format='%.4f')

# write header
with open(pivot_table,'w') as f:
    d = one_gene(protein_list[0])
    d.to_csv(f, header = True, float_format = '%.4f')

from multiprocessing import Pool
#p = Pool(8)
#print(p.map(write_to, protein_list[1:]))
for i in protein_list[1:]:
    write_to(i)


cur.close()
conn.close()
