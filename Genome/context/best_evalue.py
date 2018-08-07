import psycopg2
from Genome.context.config import config

# specify the following params
table_name = 'blastp_out'

# connect to database
params = config()
#params['database']='hermuba' # test
conn = psycopg2.connect(**params)
cur = conn.cursor()

# select
cur.execute("""
SELECT t.qseqid,t.target_genome,t.sseqid,t.evalue
INTO {0}
FROM (SELECT {1}.sseqid, {1}.target_genome, {1}.evalue, {1}.qseqid,
      MIN(evalue) over (PARTITION by {1}.qseqid, {1}.target_genome, {1}.sseqid) as max_evalue
      FROM {1}) t
WHERE t.evalue = t.max_evalue

""".format(table_name + '_max_evalue', table_name))




conn.commit()








cur.close()
conn.close()
