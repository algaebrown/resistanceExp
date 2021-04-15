import pandas as pd
import networkx as nx
import os

#### OUTPUT #####
fig_path = '/nas2/users/hermuba/fig'
data = pd.read_csv('~/nas2/integrate_net/rf.csv', index_col = 0)


# load gene annotation
base_path = '/home/hermuba/nas2/resist_subnet/'
annotation_df = os.path.join(base_path, 'gold_anno.csv')
gold_anno = pd.read_csv(annotation_df)
gold_anno.set_index('gene_id', inplace = True)
gold_anno_df = pd.read_pickle('/home/hermuba/nas2/parsed_anno/ecoli.gold_anno_df') # GO term in set 
gold_anno['GO'] = gold_anno['Unnamed: 0'].map(gold_anno_df['GO'])
gold_anno.index.set_names('Node', inplace = True)
gold_anno_str = gold_anno.copy()
gold_anno_str.index = [str(s) for s in gold_anno_str.index]
gold_anno_str['GO'] = gold_anno_str['GO'].astype(str)

# build_subnetwork
from glob import glob
scoary_result = '/nas2/users/hermuba/scoary'
# list of antibiotics
abx_list = [x.split('/')[-1].split('_')[0] for x in glob(scoary_result+'/*.results.csv')]

def read_scoary(abx):
    fname = os.path.join(scoary_result,'{}_08_02_2021_1335.results.csv').format(abx)
    df = pd.read_csv(fname, header = 0, index_col = 0)
    return df
def filter_scoary(df):
    
    return df.loc[(df['Benjamini_H_p']<0.05)& (df['Odds_ratio']>8)]

# extract subnet
net_path = os.path.join(fig_path, 'subnets.xlsx')
writer = pd.ExcelWriter(net_path, engine='xlsxwriter')

for abx in abx_list:
    resist_genes = gold_anno.loc[gold_anno['cluster'].isin(filter_scoary(read_scoary(abx)).index.tolist())].index.tolist()
    subnet = data.loc[(data['source'].isin(resist_genes)) & (data['target'].isin(resist_genes)) & (data['total_score']>0.6)]
    subnet.to_excel(writer, sheet_name = abx)
writer.save()
