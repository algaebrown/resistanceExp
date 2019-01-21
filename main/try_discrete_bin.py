# pivot
pivot = 'blastp_out_max_evalue_pivot.smpl'

from Genome.context.discretise import *

# discretize using different bins
for i in [5,10,20,40,60,80]:
    run_chunkwise('eskape_blastp_out_max_evalue_pivot.smpl', ordinary, 'eskape', bins = i)
