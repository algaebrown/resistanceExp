import psycopg2
import math
from Genome.context.config import config
params = config()

def find_second_best(db, in_table):
    # written for test
    params['database'] = db

    # connection
    conn=psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute("""
    select t.e from (select to_char(evalue,'EEEE') as e,dense_rank() over (order by evalue ASC) as dense_rank from blastp_out_max_evalue) as t where t.dense_rank = 2;
    """)

    second = cur.fetchone()

    # close
    cur.close()
    conn.close()

    #transform
    number = float(second[0]) # it's returned as str in tuple
    power = -math.log(number)

    # ceiling so that there will not be anythin > 1
    ceil_power = math.ceil(power)

    return(ceil_power)


def transform_evalue(second_best, evalue):
    if evalue == 0:
        return(1)
    if evalue >= 1:
        return(0)
    else:
        return(math.log(evalue)/-(second_best))
