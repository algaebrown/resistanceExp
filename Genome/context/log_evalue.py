# convert evalue to log evalue

# specify these params
table_name = 'archaea_blastp_out_max_evalue'

# import to connect to db
import psycopg2
from Genome.context.config import config
params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# use eskape_blastp_out as second
# eskape second best = 6e-317
# refseq second best = 3e-316
from Genome.context.transform_evalue import *
second = find_second_best('cofunctional', 'eskape_blastp_out_max_evalue')

# a temporary role for root for permission of plpythonu
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
cur.close()
conn.close()
