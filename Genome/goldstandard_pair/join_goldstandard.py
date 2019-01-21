# script to join experimetnal value to gold standard pairs
gold_std= "tf_intersect_go"
gold_std2 = "tf_intersect_pathway"

# could be anything; eskape_mu
exp_table="refseq_ordinary_40"



import psycopg2
from Genome.context.config import config


# left join to exp_table
def replace_id(exp_table, c, conn):
    c.execute("""
    alter table {0}
    add column gene_one_id text,
    add column gene_two_id text
    """.format(exp_table))

    conn.commit()

    c.execute("""
    update {0}
    set gene_one_id = qseqid_id_mapper.qseqid
    from qseqid_id_mapper
    where {0}.gene_one = qseqid_id_mapper.new_id""".format(exp_table))
    c.execute("""
    update {0}
    set gene_two_id = qseqid_id_mapper.qseqid
    from qseqid_id_mapper
    where {0}.gene_two = qseqid_id_mapper.new_id""".format(exp_table))

    conn.commit()
    c.execute("""
    alter table {0}
    drop column gene_one,
    drop column gene_two
    """. format(exp_table))

    conn.commit()
    c.execute("""
    alter table {0}
    rename column gene_one_id to gene_one
    """.format(exp_table))
    conn.commit()

    c.execute("""
    alter table {0}
    rename column gene_two_id to gene_two
    """.format(exp_table))
    conn.commit()



def left_join(exp_table, gold_std, c, conn):

    col_name = 'gd_' + exp_table.split('_')[-1] # set column name for multiple sets of goldstandard

    c.execute("""
    alter table {0}
    add column {1} boolean
    """.format(exp_table, col_name))

    conn.commit()

    c.execute("""
    update {0}
    set {2} = {1}.goldstandard
    from {1}
    where
    ({0}.gene_one = {1}.gene_one and {0}.gene_two = {1}.gene_two)
    or
    ({0}.gene_one = {1}.gene_two and {0}.gene_two = {1}.gene_one)
    """.format(exp_table, gold_std, col_name))

    conn.commit()

conn = None
try:
    params = config()
    #params['database'] = 'hermuba'
    #exp_table = 'refseq_mu_test'
    #### for test

    # connect
    print('connect to db')
    conn = psycopg2.connect(**params)
    c = conn.cursor()

    # run
    #print("replacing ID") #### needed when doing refseq
    #replace_id(exp_table, c, conn)
    print("join table with gd1")
    left_join(exp_table, gold_std, c, conn)
    print("join table with gd2")
    left_join(exp_table, gold_std2, c, conn)

except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()
