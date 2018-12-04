#
goldstandard = '/home/hermuba/data0118/goldstandard/tf_intersect'

phylo_path = '/home/hermuba/data0118/mutual_info/'

refseq_test = phylo_path + 'blastp_out_max_evalue_ordinary_mutual'
eskape_test = phylo_path + 'eskape_blastp_out_max_evalue_ordinary_mutual'

# database parameters
table_name = 'LLS'

# import
import psycopg2
from Genome.context.config import config

# put into
def create_table_from_csv(c, conn, d_columns, col_types, table_name, csv):
    column_str = ''
    for col in d_columns:
        column_str = column_str + col + ' ' + col_types + ','
    print(column_str[:-1])
    # create table
    c.execute("""
    CREATE TABLE {0}(
        gene_one text,
        gene_two text,
        {1}
    )
    """.format(table_name, column_str[:-1])) # remove the last ','

    conn.commit()
    print(csv)
    # put the tsv/csv
    with open(csv) as f:
        next(f) # skip header4
        c.copy_from(f, table_name, sep = ',')
    conn.commit()

# wrap for each kind of table
def gold_table(c, conn, csv, gold_name):
    create_table_from_csv(c, conn, ['goldstandard'], 'boolean', gold_name, csv)

def mutual_info(c, conn, csv, name):
    create_table_from_csv(c, conn, ['mutual_info', 'nrm_mutual'], 'decimal', name, csv)


# connecting to db
conn = None
try:
    params = config()

    # test
    params['database'] = 'hermuba'

    # connect
    print('connect to db')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # run
    #gold_table(cur,conn, goldstandard, 'tf_intersect')
    #mutual_info(cur,conn, refseq_test, 'refseq_mu')
    mutual_info(cur,conn, eskape_test, 'eskape_mu')

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
