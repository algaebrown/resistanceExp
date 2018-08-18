# input: postgresql blastp_out_max_evalbue table, with qseqid, evalue, target genome
# output:

import psycopg2
from Genome.context.config import config

params = config()
params['database'] = 'hermuba' ##test

table_name = 'blastp_abs'
in_table = 'blastp_out_max_evalue'
conn = psycopg2.connect(**params)
cur = conn.cursor()

cur.execute("""
SELECT DISTINCT qseqid

FROM {0}
""".format(in_table))
row_list = [i[0] for i in cur.fetchall()]


def two_genes(gene_one, gene_two):
    def add_quote(gene):
        return('\'' + gene + '\'')

    row_string = '\"' + gene_one + '\"'+ 'decimal,' + '\"'+ gene_two +'\"'+ 'decimal'
    cur.execute("""
    select * from crosstab($$select target_genome,qseqid,evalue from {0}
    where qseqid = {1} or qseqid = {2}$$)
    as t(target_genome text, {3})

    """.format(in_table, add_quote(gene_one), add_quote(gene_two), row_string))
    x = cur.fetchall()
    return(x)

x = two_genes('JMUY01000001_12314386703', 'JMUY01000001_6314386703')
conn.commit()
cur.close()
conn.close()
