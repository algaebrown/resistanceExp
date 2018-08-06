# add system path
import sys
sys.path.append('/home/hermuba/resistanceExp/')

# specify those params:
table_name = 'eskape'

import psycopg2
import Genome.context.config

def blastp_to_table(c, conn):
    # create table
    c.execute("""
    CREATE TABLE %s (

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
        stitle text,
        qtitle text


        )
    """, table_name)
    conn.commit()


    # read tsv
    #import csv
    #r = csv.reader(open("/home/hermuba/data0118/main.tsv"), delimiter = '\t')

    # insert line by line
    #for t in r:
    #    c.execute("INSERT INTO blastp_out VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s%s,%s)", t)

    # instead use copy_form
    with open("/home/hermuba/data0118/main.tsv") as f:
    #with open("/home/hermuba/data0118/test.tsv") as f:
        c.copy_from(f, 'blastp_out', sep = '\t')
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

    # insert command
    blastp_to_table(cur,conn)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
