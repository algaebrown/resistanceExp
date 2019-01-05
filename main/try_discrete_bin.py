# pivot
pivot = 'blastp_out_max_evalue_pivot.smpl'

from Genome.context.discretise import run_chunkwise

# discretize using different bins
for i in [35,45,55]:
    run_chunkwise('blastp_out_max_evalue_pivot.smpl', ordinary, 'refseq', bins = i)
