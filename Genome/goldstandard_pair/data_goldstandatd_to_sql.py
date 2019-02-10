# here are the paths
goldstandard = '/home/hermuba/data0118/goldstandard/tf_intersectpathway'
phylo_path = '/home/hermuba/data0118/mutual_info/'

# here are the input files
refseq_test = phylo_path + 'blastp_out_max_evalue_pivot_ordinary40_mutual'
eskape_test = phylo_path + 'eskape_blastp_out_max_evalue_ordinary_mutual'
domain = '/home/hermuba/data0118/domain_weight_mutual'
string = '/home/hermuba/data0118/goldstandard/EC_string_sim'


# database parameters
# table_name = 'LLS'

# import
import psycopg2
from Genome.context.config import config

# put into
def create_table_from_csv(c, conn, d_columns, col_types, table_name, csv):
    print('creating table')

    column_str = ''
    for col in d_columns:
        column_str = column_str + col + ' ' + col_types + ','
    print('columns created are '+ column_str[:-1])
    # create table
    c.execute("""
    CREATE TABLE {0}(
        gene_one text,
        gene_two text,
        {1}
    )
    """.format(table_name, column_str[:-1])) # remove the last ','

    conn.commit()
    print('makeing '+csv+ ' into psql')
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

def weighted_mutual(c,conn, csv, name):
    create_table_from_csv(c, conn, ['domain_weighted'], 'decimal', name, csv)

def string_db(c,conn,csv,name):
    create_table_from_csv(c, conn, ['string_score'], 'smallint', name, csv)

# connecting to db
conn = None
try:
    params = config()

    # test
    #params['database'] = 'hermuba'

    # connect
    print('connect to db')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # run
    print('importing csv')
    #weighted_mutual(cur, conn, domain, 'domain')
    string_db(cur, conn, string, 'string_db')
    #gold_table(cur,conn, goldstandard, 'tf_intersect_pathway')
    #mutual_info(cur,conn, refseq_test, 'refseq_ordinary_40')
    #mutual_info(cur,conn, eskape_test, 'eskape_mu')

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
