# check database

import unittest
import psycopg2
import Genome.context.config import config

# db params
params = config()

def range_trans_evalue(db,table):
    params['database'] = db
    conn = psycopg2.connect(**params)
    cur = conn.cursor

    cur.execute("""
    select max(trans_evalue), min(trans_evalue) from {0}
    """)

    t = cur.fetchone()
    max_t = float(t[0])
    min_t = float(t[1])

    cur.close()
    conn.close()

    return(max_t, min_t)

def count_trans_evalue(db, table):
    params['database'] = db
    conn = psycopg2.connect(**params)
    cur = conn.cursor

    cur.execute("""
    select count(trans_evalue), count(evalue) from {0}
    """)

    t = float(cur.fetchone()[0])
    e = float(cur.fetchone()[1])

    return(t==e)

class TestDb(unittest.TestCase):
    def test_trans_count(self):
        self.assertTrue(count_trans_evalue('cofunctional', 'blastp_out_max_evalue'))
        self.assertTrue(count_trans_evalue('cofunctional', 'eskape_blastp_out_max_evalue'))


    def test_trans_range(self):
