# convert evalue to log evalue

# specify these params
in_table = 'blastp_out_max_evalue'

# import
import psycopg2
from Genome.context.config import config

params = config()
#params['database'] = 'hermuba' ##test

conn = psycopg2.connect(**params)
cur = conn.cursor()

cur.execute("""
SET ROLE mydba
""") # a temporary role for root for permission of plpythonu

cur.execute("""
CREATE FUNCTION log_evalue (a decimal)
  RETURNS decimal
AS $$
if a >= 1:
    return(0)
if a <= 0:
    print(1)
else:
    import math
    return(math.log(a)/(-415))
$$ LANGUAGE plpythonu;

""")

conn.commit()

cur.close()
conn.close()
