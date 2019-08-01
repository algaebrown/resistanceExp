# to map resfam annotation to ARO

# read annotation files
gold_anno_path = '/home/hermuba/data0118/goldstandard/ec_rmplasmid_node_anno_df'
aro = '/home/hermuba/data0118/ontologies/aro.tsv'
resfam_metadata = '/nas/hermuba/180102_resfams_metadata_updated_v122.xlsx'
resfam_file = '/home/hermuba/data0118/cdhit/Escherichia0.70rm_plasmid-resfam'

import pandas as pd
gold_anno = pd.read_pickle(gold_anno_path)
resfam_anno = pd.read_excel(resfam_metadata, skiprows = 3, header = 0, index_col = 0)

from Genome.annotate_parser.parse_hmm import parse_hmm
resfam = parse_hmm(resfam_file)

# merge resfam ID with annotation
resfam['resistance_class'] = resfam['query_acc'].map(resfam_anno['Mechanism Classification'])
resfam['abx_class'] = resfam['query_acc'].map(resfam_anno['Antibiotic Classification (Resfam Only)'])


# dataframe
df = pd.DataFrame(index = resfam['target name'].unique(), columns = resfam['resistance_class'].unique())
for i in resfam.index:
    df.loc[resfam.loc[i, 'target name'], resfam.loc[i, 'resistance_class']] = True
df = df.fillna(False)

# write to file
df.to_csv('/home/hermuba/data0118/resfam_anno.csv')

# abx class
df = pd.DataFrame(index = resfam['target name'].unique(), columns = resfam['abx_class'].unique())
for i in resfam.index:
    df.loc[resfam.loc[i, 'target name'], resfam.loc[i, 'abx_class']] = True
df = df.fillna(False)
df.to_csv('/home/hermuba/data0118/resfam_anno_abx.csv')
