import pandas as pd
from glob import glob
import os
from Bio import SeqIO
import pickle
from itertools import chain

#### INPUT #####
annotation_df = '/nas2/users/hermuba/parsed_anno/ecoli.gold_anno_df'
scoary_result = '/nas2/users/hermuba/scoary'
repr_faa_file = '/nas2/users/hermuba/cdhit/ecoli' # representing genes from CD-hit

target_refseq_dir = '/nas2/users/hermuba/sampled_refseq'
target_eskape_dir = '/nas2/users/hermuba/sampled_eskape'

##### OUTPUT #######
outdir = '/nas2/users/hermuba/resist_subnet'
# directory for each subnet
refseq_dir = os.path.join(outdir, 'refseq')
eskape_dir = os.path.join(outdir, 'eskape')


##### SELECT RELEVANT GENES #######
# read annotation file
gold_anno = pd.read_pickle(annotation_df)
# list of antibiotics
abx_list = [x.split('/')[-1].split('_')[0] for x in glob(scoary_result+'/*.results.csv')]

def read_scoary(abx):
    fname = os.path.join(scoary_result,'{}_08_02_2021_1335.results.csv').format(abx)
    df = pd.read_csv(fname, header = 0, index_col = 0)
    return df
def filter_scoary(df):
    
    return df.loc[(df['Benjamini_H_p']<0.05)& (df['Odds_ratio']>8)]

all_resistant_genes = set()
for abx in abx_list:
    resist_cluster = filter_scoary(read_scoary(abx)).index.tolist()
    all_resistant_genes.update(resist_cluster)

print('selected {} antibiotic resistant associated genes '.format(len(all_resistant_genes)))

# also sample some some core genes
sampled_core = gold_anno.loc[gold_anno['core'], 'cluster'].sample(1000).tolist()

selected_genes = all_resistant_genes.union(set(sampled_core))
print('seclcted 1000 core genes')


##### GENERATE FASTA #######
set_of_genes = gold_anno.loc[gold_anno['cluster'].isin(selected_genes)].index.tolist()
outfaa = os.path.join(outdir, 'selected.faa')
selected_records = []
with open(repr_faa_file, 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        if record.id in set_of_genes:
            selected_records.append(record)
SeqIO.write(selected_records, outfaa, 'fasta')

##### REFSEQ/ESKAPE CO-INHERITANCE NETWORK #######
for tdir, odir in zip([target_eskape_dir, target_refseq_dir],[eskape_dir, refseq_dir]):
    try:
        os.mkdir(odir)
    os.system('python ~/co-inheritance/coinheritance/main.py -t {} -g {} -o {} -b 200 -s mutual_info -p 16'.format(
        tdir, outfaa, odir
    )) # params are chosen based on 9_network_hyperparam_fit


##### GOSIM #######
gold_anno_subset = gold_anno.loc[gold_anno['cluster'].isin(selected_genes)]
# write the gene_id
gene_id_mapper = pickle.load(open(os.path.join(outdir, 'eskape', 'gene_id.pickle'), 'rb'))
gene_id_mapper2 = pickle.load(open(os.path.join(outdir, 'refseq', 'gene_id.pickle'), 'rb'))
assert gene_id_mapper == gene_id_mapper2

gold_anno_subset['gene_id'] = gold_anno_subset.index.map(gene_id_mapper)
gold_subset_out = os.path.join(outdir, 'gold_anno.csv')
gold_anno_subset.to_csv(gold_subset_out)

# run GO term similarity score
os.system('Rscript --vanilla ~/resistanceExp/main/8_GOsim.R {} {}'.format(
gold_subset_out, os.path.join(outdir, 'gosim.csv')
))


##### DOMAIN #######
# for gold_anno domain
from scipy.sparse import csr_matrix, lil_matrix, save_npz
def domain_to_pivot(gold_anno, col = 'domain', index = 'gene_id', term_mapper = None):
    '''
    Convert doamin in gold_anno into np sparse matrix
    '''
    with_data = gold_anno.loc[gold_anno[col].notnull()]
    all_terms = set(list(chain.from_iterable(with_data[col].tolist())))
    
    # mapping term to integer
    if term_mapper:
        pass
    else:
        term_mapper = {}
        for i, term in enumerate(all_terms):
            term_mapper[term]=i
    
    # initialize sparse matrix
    ma = lil_matrix((gold_anno[index].max(), len(term_mapper)))
    
       
    for i, terms in zip(with_data[index], with_data[col]):
        gene_id = [i]
        target_id = [term_mapper[t] for t in terms if t in term_mapper.keys()]
        ma[gene_id, target_id] = [1]*len(target_id)
        
    
    return ma, term_mapper

    
ma, term_mapper = domain_to_pivot(gold_anno_subset)
save_npz(os.path.join(outdir, 'domain', 'domain_binary.npz'), ma.tocsr())   

# Global domain matrix
gold_anno['gene_id'] = np.arange(gold_anno.shape[0])
ma_glob, term_mapper = domain_to_pivot(gold_anno, term_mapper = term_mapper)
save_npz(os.path.join(outdir, 'domain', 'domain_binary_global.npz'), ma.tocsr())   

assert ma.shape[1] == ma_glob.shape[1]


os.system('python ~/weighted_mutual/calc_score_async.py --input {} --global {} -o {} -p 9'.format(
    os.path.join(outdir, 'domain', 'domain_binary.npz'),
    os.path.join(outdir, 'domain', 'domain_binary_global.npz'),
    os.path.join(outdir, 'domain')
))

######## STRING ###########
os.system('python ~/resistanceExp/Genome/string/extract_existing_net.py /nas/hermuba/data0118/map_to_exist_net/511145.protein.sequences.v11.0.fa.gz  /nas/hermuba/data0118/map_to_exist_net/511145.protein.links.full.v11.0.txt ../gold_anno.csv string ../selected.faa ../'