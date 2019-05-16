# add system path



# specify those params:
table_name = 'blastp_out'
infile = '/home/hermuba/data0118/concat_phylo/refseq.tab'

import psycopg2
from Genome.context.config import config
import math

def blastp_to_table(c, conn, infile, table_name):
    # create table
    c.execute("""
    CREATE TABLE {0} (

        target_genome text,
        qseqid text,
        qlen integer,
        sseqid text,
        slen text,
        sstart integer,
        send integer,
        qstart integer,
        qend integer,
        evalue decimal,
        bitscore decimal,
        stitle text



        )
    """.format(table_name))
    conn.commit()

    # instead use copy_form
    with open(infile) as f:

        c.copy_from(f, table_name, sep = '\t')
    conn.commit()

def max_evalue(c, conn, table_name):

    c.execute("""
    SELECT t.qseqid,t.target_genome,t.sseqid,t.evalue
    INTO {0}
    FROM (SELECT {1}.sseqid, {1}.target_genome, {1}.evalue, {1}.qseqid,
      MIN(evalue) over (PARTITION by {1}.target_genome, {1}.qseqid) as max_evalue
      FROM {1}) t
    WHERE t.evalue = t.max_evalue

    """.format(table_name + '_max_evalue', table_name))

    conn.commit()


# connect to database
conn = None
try:
    # read the connection parameters
    params = config()

    # test
    #params['database'] = 'hermuba'

    # connect
    print("connecting to the DB")
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # write to database
    #print("writing to database")
    #blastp_to_table(cur,conn, infile, table_name)

    # find max evalue
    #print("finding max evalue")
    #max_evalue(cur, conn, table_name)

    # find second best evalue
    print("finding second best evalue of all gene pairs")
    from Genome.context.transform_evalue import *
    second = find_second_best(cur, conn, table_name + '_max_evalue')
    print("second best evalue is "+ str(second))

    # transform based on second best evalue
    transform_evalue(cur, conn, table_name + '_max_evalue', second)
    print("transformation complete")



except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
