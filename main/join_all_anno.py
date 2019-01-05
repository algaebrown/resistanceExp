'''
Initially Created: 2018-12-17
Last Modified: 2018-12-17
Purpose: To join information from interpro other representing gene annotations
'''
# read InterPro file
import Genome.goldstandard_pair.parse_interpro_out as ipr
infile = '/home/hermuba/data0118/interpro/ec70_20180929'
df = ipr.parse(infile)

# read nr annotation
import pandas as pd
pan_blast = pd.read_pickle("/home/hermuba/data0118/ecoli70_dmnd_df")
pan_blast = pan_blast.set_index('qseqid')

# read whole pan-genome file
real_pan = pd.read_csv("/home/hermuba/data0118/cdhit/clstr/cluster_detail/Escherichia0.70.clstr.tab", sep = '\t')
real_pan = real_pan.set_index('representing_gene')

# read card annotation
card = pd.read_pickle('/home/hermuba/data0118/cdhit/card/Escherichia0.70_df')

# convert to series-set format
go = ipr.extract_term(df,'goterm')
pathway = ipr.extract_term(df,'pathway')
ipr_ac = ipr.extract_term(df,'ipr_accession') #domain

card_s = ipr.extract_card(card)

# join dataframe
gold_anno = pd.DataFrame(index = real_pan.index, columns = ['pathway', 'GO', 'nr', 'cluster', 'card','domain'])
gold_anno['pathway'] = pathway
gold_anno['GO'] = go
gold_anno['card'] = card_s
gold_anno['domain'] = ipr_ac
gold_anno['cluster'] = real_pan['Cluster']
gold_anno.loc[pan_blast.index, 'nr'] = pan_blast['stitle']
from Genome.pangenome_annotate.hypothetical import identify_hypothetical
hypo = identify_hypothetical(pan_blast)
gold_anno.loc[hypo.index,'hypo_nr'] = hypo['hypothetical'].fillna(False)

print(gold_anno.count())
