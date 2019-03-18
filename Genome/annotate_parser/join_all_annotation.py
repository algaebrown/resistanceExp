import pandas as pd
gold_anno = pd.read_pickle('/home/hermuba/data0118/goldstandard/node_anno_df')
# with pathway, GO, nr, cluster, card, domain, hypo_nr

# binary card
gold_anno['is_card']=gold_anno['card'].notnull()
gold_anno['is_card'] = gold_anno['is_card'].fillna(False)

# add pan-genome stats
pan = pd.read_csv('/home/hermuba/data0118/cdhit/clstr/pangenome_df/Escherichia0.70.clstr.csv', index_col = 0, header = 0)
count = pan.merge(gold_anno[['cluster', 'GO']], left_index = True, right_on = 'cluster').drop(columns = ['GO', 'cluster'], axis = 1).sum(axis = 1)
gold_anno['count'] = count # how many genome has that Gene

# defining core genes: 1574 by essential gene: greatest decrease of bins

gold_anno.loc[gold_anno.loc[gold_anno['count'] >1574].index, 'core'] = True
gold_anno['core'] = gold_anno['core'].fillna(False)

# RESFAM by Gautam Dantas lab
resfam = pd.read_pickle('/home/hermuba/data0118/EC70_resfam_df')
# each gene has more than one domain
resfam_comb = resfam.groupby(by = 'target name')['query name'].apply(lambda x: "{%s}" % ', '.join(x))
gold_anno['resfam'] = resfam_comb

# loose_card
loose_card = pd.read_pickle('/home/hermuba/data0118/cdhit/EC70_loose_card_df')
i = loose_card['ORF_ID'].str.split(' ').str[0]
loose_card.set_index(i, inplace = True)

# parse best ARO hit category
parsed_category = loose_card['Best_Hit_ARO_category'].apply(lambda x: x.split('; '))
flattened_list = [y for x in parsed_category for y in x]
all_category = pd.DataFrame(index = loose_card.index, columns = list(set(flattened_list)))
n = 0
for p in parsed_category:
    i = loose_card.index[n]
    all_category.loc[i, p] = True

    n += 1
all_category.fillna(False, inplace = True)



gold_anno['loose_best_ARO'] = loose_card['Best_Hit_ARO']
gold_anno['loose_ARO'] = loose_card['ARO']

# mobile elements
aclame = pd.read_pickle('/home/hermuba/data0118/cdhit/EC_aclame_df')
aclame.drop_duplicates(subset = 'qseqid', inplace = True)
aclame.set_index('qseqid', inplace = True)
gold_anno['aclame_title'] = aclame['stitle']
gold_anno.loc[gold_anno['aclame_title'].notnull(), 'is_aclame'] = True
gold_anno['is_aclame'] = gold_anno['is_aclame'].fillna(False)

# COF
cog = pd.read_pickle('/home/hermuba/data0118/cdhit/EC70_cog_df')
total = pd.merge(cog, gold_anno, left_index = True, right_index = True, how = 'outer')

# drug target # ARO:3000708 is_in, derive_from,
drug = pd.read_pickle('/home/hermuba/data0118/cdhit/EC70_drug_target_df')
drug.set_index('qseqid', inplace = True)
total['drug_target'] = drug['stitle']
total.loc[drug.index, 'is_drug_target'] = True
total['is_drug_target'] = total['is_drug_target'].fillna(False)
