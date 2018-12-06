# to parse cdhit files

cog_list = '/home/hermuba/COGmapper/COG.list'
out = '/home/hermuba/resistanceExp/EcoliGenomes/cdhitResult/ec0913.COG_annotation'

import pandas as pd
cog = pd.DataFrame(columns = ['cog_category'])

output = pd.DataFrame(columns = ['cog_ID'])

with open(cog_list) as cog_list:
    for line in cog_list:
        category = line.split('\t')[0].replace('[', '').replace(']', '').replace('\ufeff', '') # [AE] or [A]
        ID = line.split('\t')[1].replace('\n', '') # COG0001
        cog.loc[ID, 'cog_category'] = category
with open(out) as o:
    for line in o:
        gene_header = line.split('\t')[0]
        cog_ID = line.split('\t')[1].split('.')[1]
        output.loc[gene_header, 'cog_ID'] = cog_ID

df = pd.merge(output, cog, left_on = 'cog_ID', right_index = True)
df.to_pickle('\home\hermuba\resistantExp\EcoliGenomes\cdhitResult\ec0913_coganno_df')