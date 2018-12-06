'''
Initial Date: 2018-11-04
Last modified: 2018-11-04
Author: Hsuan-lin Her
Purpose: To calcualte hypothetical protein portion in 6 pan-genomes
'''

# input file: 6 pan-genomes' representing gene, use diamond blastp against nr database
input_path = '/home/hermuba/data0118/cdhit/dmnd_nr/'
output_path = '/home/hermuba/data0118/cdhit/cluster_blast_hypo'

from Genome.annotate_parser.parse_blast import parse_diamond
from Genome.pangenome_annotate.hypothetical import *

def combined(species):
    df = parse_diamond(input_path + species + '0.70')
    df = identify_hypothetical(df)

    return(df)

pangenome_df_path = '/home/hermuba/data0118/cdhit/clstr/pangenome_df/'
def pangenome_size(species):
    '''
    return the size of pangenome by counting how many rows
    '''
    with open(pangenome_df_path + species + '0.70.clstr.csv') as f:
        for i, l in enumerate(f):
            pass
        return(i) # i+1 lines; but the first line is header

# main
for sps in ['Escherichia', 'Acinetobacter', 'Enterobacter', 'Klebsiella', 'Citrobacter']:
    df = combined(sps)
    df.to_pickle(output_path + sps + '0.70_nr_hypo_df')
    size = pangenome_size(sps)

    # percentage
    hypo_count = df['hypothetical'].sum()

    print(sps, size, hypo_count, hypo_count/size)
