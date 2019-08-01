import pandas as pd
# specify input file path
pan_abs = '/home/hermuba/data0118/cdhit/clstr/pangenome_df/Escherichia0.70rm_plasmid.clstr.csv'
pan_detail = '/home/hermuba/data0118/cdhit/clstr/cluster_detail/Escherichia0.70rm_plasmid.clstr'
card = '/home/hermuba/data0118/cdhit/card/Escherichia0.70rm_plasmid.txt'
resfam_file = '/home/hermuba/data0118/cdhit/Escherichia0.70rm_plasmid-resfam'
aclame_file = '/home/hermuba/data0118/cdhit/Escherichia0.70rm_plasmid-aclame'
drug_file = '/home/hermuba/data0118/cdhit/Escherichia0.70rm_plasmid-drug_target'
nr_file = '/home/hermuba/data0118/cdhit/dmnd_nr/Escherichia0.70rm_plasmid'
cog_file = '/home/hermuba/data0118/cdhit/Escherichia0.70rm_plasmid.COG_annotation'
interpro_file = '/home/hermuba/data0118/interpro/all'
cog_list = '/home/hermuba/bin/COGmapper/COG.list'

# read gene_id and cluster
gold_anno = pd.read_csv(pan_detail, names = ['cluster', 'Gene ID'])
gold_anno.set_index('Gene ID', inplace = True)


# calculate count
from Genome.pangenome_intrinsic_info.count_core_acc import gene_distribution, extended_core
count, pan_size, df = gene_distribution(pan_abs)
count.name = 'count'
gold_anno = gold_anno.merge(count, left_on = 'cluster', right_index = True, copy = False)

# define core
import matplotlib.pyplot as plt
n, bins, patches = plt.hist(count)
thres = extended_core(n, bins)
gold_anno.loc[gold_anno.loc[gold_anno['count'] >thres].index, 'core'] = True
gold_anno['core'] = gold_anno['core'].fillna(False)

# parse card
from Genome.annotate_parser.card_complete_parse import parse_card, process_card
c = parse_card(card)
c = process_card(c)
i = c['ORF_ID'].str.split(' ').str[0]
c.set_index(i, inplace = True)

# find strict and loose
strict_card = c.loc[c['CUT_OFF'] != 'Loose']
loose_card = c.loc[c['CUT_OFF'] == 'Loose']

# merge into gold_anno
gold_anno['loose_best_ARO'] = loose_card['Best_Hit_ARO']
gold_anno['loose_ARO'] = loose_card['ARO']
gold_anno['strict_best_ARO'] = strict_card['Best_Hit_ARO']
gold_anno['strict_ARO'] = strict_card['ARO']

# binary card
gold_anno['is_card']=gold_anno['strict_ARO'].notnull()
gold_anno['is_card'] = gold_anno['is_card'].fillna(False)

# parse ARO category
parsed_category = strict_card['Best_Hit_ARO_category'].apply(lambda x: x.split('; '))
flattened_list = [y for x in parsed_category for y in x]
all_category = pd.DataFrame(index = strict_card.index, columns = list(set(flattened_list)))
n = 0
for p in parsed_category:
    i = strict_card.index[n]
    all_category.loc[i, p] = True

    n += 1
all_category.fillna(False, inplace = True)
all_category.to_csv('/home/hermuba/data0118/Escherichia0.70rm_plasmid_card.csv')


# RESFAM by Gautam Dantas lab
from Genome.annotate_parser.parse_hmm import parse_hmm
resfam = parse_hmm(resfam_file)
# each gene has more than one domain
resfam_comb = resfam.groupby(by = 'target name')['query name'].apply(lambda x: "{%s}" % ', '.join(x))
gold_anno['resfam'] = resfam_comb

# mobile elements
from Genome.annotate_parser.parse_blast import *
aclame = parse_diamond(aclame_file)
aclame = aclame_preprocess(aclame)
aclame.drop_duplicates(subset = 'qseqid', inplace = True)
aclame.set_index('qseqid', inplace = True)
gold_anno['aclame_title'] = aclame['stitle']
gold_anno.loc[gold_anno['aclame_title'].notnull(), 'is_aclame'] = True
gold_anno['is_aclame'] = gold_anno['is_aclame'].fillna(False)

# nr
nr = parse_diamond(nr_file)
nr.set_index('qseqid', inplace = True)
gold_anno.loc[nr.index, 'nr'] = nr['stitle']

# hypothetical protein
from Genome.pangenome_annotate.hypothetical import identify_hypothetical
nr = identify_hypothetical(nr)
gold_anno.loc[nr.index, 'hypo_nr'] = nr['hypothetical']

# drug target: is_in, derive_from
drug = parse_diamond(drug_file)
drug.set_index('qseqid', inplace = True)
gold_anno['drug_target'] = drug['stitle']
gold_anno.loc[drug.index, 'is_drug_target'] = True
gold_anno['is_drug_target'] = gold_anno['is_drug_target'].fillna(False)


# COG
from Genome.annotate_parser.parse_cog import COG_to_df
cog = COG_to_df(cog_list, cog_file)
total = pd.merge(cog, gold_anno, left_index = True, right_index = True, how = 'outer')

# interpro
from Genome.goldstandard_pair.parse_interpro_out import parse, extract_term
itp = parse(interpro_file)

go = extract_term(itp, 'goterm')
total['GO'] = go
path = extract_term(itp, 'pathway')
total['pathway'] = path
dm = extract_term(itp, 'ipr_accession')
total['domain'] = dm
