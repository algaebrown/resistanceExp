# cause dot in target_genome, qseqid, sseqid will cause inconvinence
# will replace it with

import psycopg2
from Genome.context.config import config

params = config()
#params['database'] = 'hermuba'

#table_name = 'blastp_out_max_evalue'

conn = psycopg2.connect(**params)
cur = conn.cursor()


def id_mapper(col):

    cur.execute("""
    SELECT DISTINCT {0}
    INTO {2}
    FROM {1}

    """.format(col, table_name, col+'_id_mapper'))

    conn.commit()

    cur.execute("""
    ALTER TABLE {0}
    ADD COLUMN new_id text
    """.format(col+'_id_mapper'))

    cur.execute("""
    UPDATE {0}
    SET "new_id" = replace({1}, '.', '')
    """.format(col+'_id_mapper', col))

    conn.commit()



    return(0)

def change_ori_table(col):
    # change the original table
    cur.execute("""
    UPDATE {0}
    SET {1} = replace({1}, '.', '')
    """.format(table_name, col))
    cur.execute("""
    UPDATE {0}
    SET {1} = replace({1}, '|', '')
    """.format(table_name, col))
    conn.commit()
    return(0)

#id_mapper('qseqid')
#id_mapper('sseqid')
#id_mapper('target_genome')

change_ori_table('qseqid')
change_ori_table('sseqid')
change_ori_table('target_genome')
cur.close()
conn.close()
