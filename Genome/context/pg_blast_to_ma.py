
# input: postgresql blastp_out_max_evalue table, with qseqid, evalue, target genome
# output:

import psycopg2
from Genome.context.config import config

params = config()
#params['database'] = 'hermuba' ##test

table_name = 'blastp_abs'
in_table = 'blastp_out_max_evalue'
conn = psycopg2.connect(**params)
cur = conn.cursor()

cur.execute("""
SELECT DISTINCT target_genome

FROM {0}
""".format(in_table))
row_list = [i[0] for i in cur.fetchall()]
row_string = ''

for row in row_list:
    row_string = row_string + '\"'+ row + '\"'+' ' + 'decimal' + ','

cur.execute("""
    SELECT *
    INTO {0}
    FROM crosstab('select qseqid, target_genome, evalue from {1}')
    AS {0}(qseqid text, {2})

    """.format(table_name, in_table, row_string[:-1]))
conn.commit()
cur.close()
conn.close()
