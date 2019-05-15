import psycopg2
import math
from Genome.context.config import config
params = config()

def find_second_best(cur, conn, table_name):

    # select the smallest and second smallest e-value
    cur.execute("""
    select t.e from (select to_char(evalue,'EEEE') as e,dense_rank() over (order by evalue ASC) as dense_rank from {0}) as t where t.dense_rank <= 2;
    """.format(table_name))

    second = cur.fetchall()

    if float(second[0][0])!= 0:
        number = float(second[0][0])
    elif float(second[1][0])!= 0:
        number = float(second[1][0])

    #transform

    power = -math.log(number)

    # ceiling so that there will not be anythin > 1
    ceil_power = math.ceil(power)

    return(ceil_power)

# a temporary role for root for permission of plpythonu
def transform_evalue(cur, conn, table_name, second):


    cur.execute("""
    SET ROLE mydba
    """)

    # create or update function
    cur.execute("""
    CREATE OR REPLACE FUNCTION log_evalue (a decimal)
    RETURNS decimal
    AS $$
    if a == 0:
        return(1)
    if a >= 1:
        return(0)
    else:
        import math
        return(math.log(a)/-({0}))


    $$ LANGUAGE plpythonu;

    """.format(str(second)))

    conn.commit()

    # reset role
    cur.execute("""
    RESET ROLE
    """)

    # add column if not exist
    cur.execute("""
    ALTER TABLE {0}
    ADD COLUMN trans_evalue decimal

    """.format(table_name))

    # update the column 'trans_evalue'
    cur.execute("""
    UPDATE {0}
    SET trans_evalue =  log_evalue(evalue)


    """.format(table_name))


    conn.commit()
