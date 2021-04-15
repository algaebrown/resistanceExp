import pandas as pd
import os
from optparse import OptionParser
parser = OptionParser()


parser.add_option("-f", "--anno", dest="anno_path",
                  help="folder with all annotation outputs")
parser.add_option("-p", "--prefix", dest="prefix",
                  help="prefix names")
parser.add_option("-c", "--cdhit", dest="cdhit",
                  help="folder containing cdhit outputs")
parser.add_option("-r", "--resfam", dest="resfam_metadata",
                  help="path to resfam metadata excel file", default = '/nas/hermuba/180102_resfams_metadata_updated_v122.xlsx')
parser.add_option("--cog", dest="cog",
                help="COG ID mapping to list", default = '/home/hermuba/bin/COGmapper/COG.list')
parser.add_option("-o", "--out", dest="outf",
                  help="path annotation output folders")
(options, args) = parser.parse_args()

# specify input file path
anno_path = args.anno_path
name = args.prefix
# specify cdhit path
cdhit_path = args.cdhit

# CD-HIT input
pan_abs = os.path.join(cdhit_path, '{}.clstr.csv'.format(name))
repr_gene = os.path.join(cdhit_path, '{}.repr.csv'.format(name)) # map gene ID to cluster id
pan_stat = os.path.join(cdhit_path,'pangenome_grow_stat.csv')

# ANNOTATION INPUT
card_file = os.path.join(anno_path, '{}.card.txt'.format(name))
resfam_file = os.path.join(anno_path, '{}.resfam'.format(name))
resfam_metadata = args.resfam_metadata # annotation of each resfam ID belongs to what category

aclame_file = os.path.join(anno_path, '{}.aclame'.format(name))
drug_file = os.path.join(anno_path, '{}.drug_target'.format(name))
nr_file = os.path.join(anno_path, '{}.nr'.format(name))
uniref_file = os.path.join(anno_path, '{}.uniref'.format(name))
cog_file = os.path.join(anno_path, '{}.COG_annotation'.format(name))
cog_list = args.cog
interpro_file = os.path.join(anno_path, '{}.interpro'.format(name))

# OUTPUT
outdir = args.outf
card_category_out = os.path.join(outdir, 'card_category.xlsx')
resfam_category_out = os.path.join(outdir, 'resfam_category.xlsx')
cog_category_out = os.path.join(outdir, 'cog_category.csv')


# read gene_id and cluster
gold_anno = pd.read_csv(repr_gene, names = ['cluster', 'Gene ID'])
gold_anno.set_index('Gene ID', inplace = True)


# import calcaulted count
from Genome.pangenome_intrinsic_info.count_core_acc import gene_distribution, extended_core
count, pan_size, df = gene_distribution(pan_abs)
count.name = 'count'
gold_anno = gold_anno.merge(count, left_on = 'cluster', right_index = True, copy = False)

# define core
with open(pan_stat) as f:
    lines = f.readlines()
thres_line = lines[1].rstrip()
thres = float(thres_line.split(' ')[4])
gold_anno.loc[gold_anno.loc[gold_anno['count'] >thres].index, 'core'] = True
gold_anno['core'] = gold_anno['core'].fillna(False)

# parse CARD annotations
from Genome.annotate_parser.card_complete_parse import parse_card, extract_ARO
card_file = os.path.join(anno_path, '{}.card.txt'.format(name))
card = parse_card(card_file)
# binary card
gold_anno.loc[card.index, 'is_card']=True
gold_anno['is_card'] = gold_anno['is_card'].fillna(False)

gold_anno['Best_Hit_ARO'] = card['Best_Hit_ARO']
gold_anno['ARO'] = card['ARO']

for category_column in ['Resistance Mechanism', 'AMR Gene Family', 'Drug Class']:
    category = extract_ARO(card, category_column = category_column)
    category.to_excel(card_category_out, sheet_name = category_column)
    
# Resfam annotations
from Genome.annotate_parser.parse_hmm import parse_hmm
resfam = parse_hmm(resfam_file)
resfam_metadata_df = pd.read_excel(resfam_metadata, skiprows=3, index_col = 0)

# select columns to add to
for col in ['Resfam Family Name', 'Antibiotic Classification (Resfam Only)', 'Mechanism Classification']:
    resfam[col]=resfam['query_acc'].map(resfam_metadata_df[col])

# resfam binary tables
for col in ['Resfam Family Name', 'Antibiotic Classification (Resfam Only)', 'Mechanism Classification']:
    resfam_cat = pd.get_dummies(resfam[['target name',col]], columns = [col], prefix = '').groupby(['target name']).sum()
    resfam_cat.to_excel(resfam_category_out, sheet_name = col.split(' (')[0])

# each gene has more than one domain
resfam_comb = resfam.groupby(by = 'target name')['query name'].apply(lambda x: "{%s}" % ', '.join(x))
gold_anno['resfam'] = resfam_comb
gold_anno['is_resfam'] = gold_anno['resfam'].notnull()

# mobile elements: aclame database
from Genome.annotate_parser.parse_blast import *
aclame = parse_diamond(aclame_file)
aclame = aclame_preprocess(aclame)
aclame.drop_duplicates(subset = 'qseqid', inplace = True)
aclame.set_index('qseqid', inplace = True)
gold_anno['aclame_title'] = aclame['stitle']
gold_anno.loc[gold_anno['aclame_title'].notnull(), 'is_aclame'] = True
gold_anno['is_aclame'] = gold_anno['is_aclame'].fillna(False)


# drug target: is_in, derive_from
drug = parse_diamond(drug_file)
drug.drop_duplicates('qseqid', inplace = True)
drug.set_index('qseqid', inplace = True)
gold_anno['drug_target'] = drug['stitle']
gold_anno.loc[drug.index, 'is_drug_target'] = True
gold_anno['is_drug_target'] = gold_anno['is_drug_target'].fillna(False)

# COG
from Genome.annotate_parser.parse_cog import COG_to_df
cog = COG_to_df(cog_list, cog_file)
gold_anno = pd.merge(cog, gold_anno, left_index = True, right_index = True, how = 'outer')
split_cog = gold_anno.loc[gold_anno['cog_category'].notnull()]['cog_category'].apply(list)
cog_df = pd.DataFrame(columns = ['J','A','K','L','B','D','Y','V','T','M','N','Z','W','U','O','C','G','E','F','H','I','P','Q','R','S','no COG'], index = gold_anno.index)

# make into 0101 table
for i in split_cog.index:
    cog_lists = split_cog[i]
    for each_category in cog_lists:
        cog_df.loc[i, each_category] = True

# find those without COG
cog_df.loc[gold_anno.loc[gold_anno['cog_category'].isnull()].index, 'no COG'] = True
cog_df.fillna(False, inplace = True)
cog_df.to_csv(cog_category_out)

# interpro
from Genome.goldstandard_pair.parse_interpro_out import parse, extract_term, seperate_by_namespace
itp = parse(interpro_file)
# GO term
go = extract_term(itp, 'goterm')
gold_anno['GO'] = go
go_df = seperate_by_namespace(go)

# merge into 1 dataframe
gold_anno = pd.merge(gold_anno, go_df, left_index = True, right_index = True, how = 'outer')

# Pathway
path = extract_term(itp, 'pathway')
gold_anno['pathway']=path

# domain
dm = extract_term(itp, 'ipr_accession')
gold_anno['domain'] = dm

# NR database annotation
nr = parse_diamond(nr_file)
nr.set_index('qseqid', inplace = True)
gold_anno.loc[nr.index, 'nr'] = nr['stitle']

# hypothetical protein
from Genome.pangenome_annotate.hypothetical import identify_hypothetical
nr = identify_hypothetical(nr)
gold_anno.loc[nr.index, 'hypo_nr'] = nr['hypothetical']

# OUTPUT
gold_anno.to_csv(os.path.join(outdir, '{}.gold_anno.csv'.format(args.prefix)))
gold_anno.to_pickle(os.path.join(outdir, '{}.gold_anno_df'.format(args.prefix)))
