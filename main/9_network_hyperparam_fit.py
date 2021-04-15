# randomly select 1000 genes with GO terms, calculate go similarity threshold, then try out different network hyperparameter
# require another package https://github.com/algaebrown/co-inheritance
import pandas as pd
import os
from Bio import SeqIO
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


##### INPUT ######
annotation_df = '/nas2/users/hermuba/parsed_anno/ecoli.gold_anno_df'
repr_faa_file = '/nas2/users/hermuba/cdhit/ecoli' # representing genes from CD-hit
refseq_dir = '/home/hermuba/data0118/refseq/prokaryotes/faa'
eskape_dir = '/home/hermuba/data0118/predicted_genes'

##### OUTPUT #######
outdir = '/nas2/users/hermuba/network_hyperparam'
new_refseq_dir = '/nas2/users/hermuba/sampled_refseq'
new_eskape_dir = '/nas2/users/hermuba/sampled_eskape'
figout = '/nas2/users/hermuba/fig/network_hyperparam'

# sample genes

gold_anno = pd.read_pickle(annotation_df)
set_of_genes = gold_anno.loc[gold_anno['GO'].notnull()].sample(1000)
set_of_genes.to_pickle(os.path.join(outdir, 'selected_gene_anno_df'))

# run GO term similarity score 
set_of_genes.to_pickle(os.path.join(outdir, 'selected_gene_anno.csv'))
gosim_path = os.path.join(outdir, 'gosim.txt')
os.system('Rscript --vanilla 8_GOsim.R {} {}'.format(
    os.path.join(outdir, 'selected_gene_anno.csv'),
    gosim_path
    )
    )


# prepare the fasta file
outfaa = os.path.join(outdir, 'selected.faa')
selected_records = []
with open(repr_faa_file, 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        if record.id in set_of_genes.index:
            selected_records.append(record)
SeqIO.write(selected_records, outfaa, 'fasta')

# select subset of target genomes
import random

def sample_target_genome(target_dir, new_genome_dir, n = 1500):
    ''' sample n target genome '''
    sampled_genome = random.sample([f for f in os.listdir(target_dir) if f.endswith('.faa')], n)
    for g in sampled_genome:
        os.system('ln -s {} {}'.format(
            os.path.join(target_dir, g),
            os.path.join(new_genome_dir, g))
                )

sample_target_genome(refseq_dir, new_refseq_dir)
sample_target_genome(eskape_dir, new_eskape_dir)

# run all possible params
os.system('~/co-inheritance/coinheritance/optimize_hyperparameter.py --target {} --gene {} --outdir {} -d 1'.format(new_refseq_dir, outfaa, os.path.join(outdir, 'refseq')))
os.system('~/co-inheritance/coinheritance/optimize_hyperparameter.py --target {} --gene {} --outdir {} -d 1'.format(new_eskape_dir, outfaa, os.path.join(outdir, 'eskape')))

# start benchmarking results
df = pd.read_csv(gosim_path, sep = ' ', names = ['gene_id1', 'gene_id2', 'gosim'], skiprows = 1)


fitting_stat = []

for target_genome in ['eskape', 'refseq']:
    for b in [10, 50, 100, 150, 200]:
        for score in ['mutual_info', 'normalized_mutual_info']:
            network = pd.read_csv(os.path.join(outdir, target_genome, b, '{}.csv'.format(score)))
            
            merged = pd.merge(df, network, left_on = ['gene_id1', 'gene_id2'], right_on = ['gene_one', 'gene_two'])
            merged['bin'] = pd.qcut(merged['mutual_info'], q =100, labels = False, duplicates = 'drop')
            
            median = merged.groupby(by = 'bin').median() ['gosim']
            r, pval = pearsonr(median.index, median.values)
            
            f, ax = plt.subplots()
            median.plot(ax = ax)
            ax.set_title('{}_{}_{}'.format(target_genome, b, score))
            ax.set_xlabel('{} bins'.format(score))
            ax.set_ylabel('median GO Sim')
            ax.text(80, 0.03, 'r={:.2f}, p={:e}'.format(r, pval))
            f.savefig(os.path.join(figout, '{}_{}_{}.png'.format(target_genome, b, score)))
            
            fitting_stat.append([target_genome, b, score, r])

stat = pd.DataFrame(fitting_stat)
stat.to_csv(os.path.join(outdir, 'hyperparam_fitting_stat.csv'))