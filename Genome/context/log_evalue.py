# convert evalue to log evalue

# specify these params
in_table = 'blastp_out_max_evalue'

# import
import psycopg2
import Genome.context.config

params = config()
params['database'] = 'hermuba' ##test

conn = psycopg2.connect(**params)
cur = conn.cursor()

cur.execute("""
CREATE FUNCTION log_evalue (a decimal)
  RETURNS decimal
AS $$
  for i in a:
      if a >= 1:
         0 ########
      else:
        import numpy as np
        return np.log(a)/415 ######
$$ LANGUAGE plpythonu;

""")

cur.commit()
cur.execute("""
SELECT evalue


""")
