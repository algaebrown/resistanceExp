import pandas as pd
norm_tmacc = pd.read_pickle("/home/hermuba/data/drug/norm_tmacc")
tmacc_pca = pd.read_pickle("/home/hermuba/data/drug/pca_tmacc")
amr_data = pd.read_pickle('/home/hermuba/data/annotated_RIS/anno_sps_df')
cluster = pd.read_pickle('/home/hermuba/data/genePredicted/cdhit/ec0102_df')
card = pd.read_pickle('/home/hermuba/data/aro_pattern_df')

# clean some data
amr_data['Antibiotic'] = amr_data['Antibiotic'].str.lower()

# join dataframe
tmacc_amr = tmacc_pca.merge(amr_data[['Genome ID', 'Measurement Value', 'Species', 'Antibiotic', 'Resistant Phenotype']] , right_on='Antibiotic', left_index = True, suffixes=('_x', '_y'))
tmacc_amr_num = tmacc_amr.loc[tmacc_amr['Measurement Value'] != 'nan']

# some numeric operation
import math
tmacc_amr_num['log_mic'] = pd.to_numeric(tmacc_amr_num['Measurement Value'])
tmacc_amr_num['log_mic'] = tmacc_amr_num['log_mic'].apply(lambda x:np.log(x)/np.log(2)) # log transformation
tmacc_amr_num = tmacc_amr_num.loc[tmacc_amr_num['log_mic'].apply(np.isfinite)]

# join gene with tmacc
all_num = tmacc_amr_num.merge(cluster, left_on = 'Genome ID', right_index = True) #using Ecoli as a test
all_num_card = tmacc_amr_num.loc[tmacc_amr_num['Species'] == 'Escherichia'].merge(card, left_on = 'Genome ID', right_index = True) #using Ecoli as a test
all_sps_card = tmacc_amr_num.merge(card, left_on = 'Genome ID', right_index = True) #using Ecoli as a test

# indexing
tmacc_id = tmacc_amr.columns[:-5]
card_id = all_num_card.columns[-189:]
cluster_id = all_num.columns[-15950:]

def itxn_correlation(df, cset1, cset2):
    itxn_corr = []
    itxn_features = pd.DataFrame()
    for col1 in cset1:
        for col2 in cset2:
            itxn = df[col1].multiply(df[col2])
            corr = df['log_mic'].corr(itxn)
            itxn_corr.append(corr)
            if corr > 0.4:
                itxn_features[str(col1)+':'+str(col2)] = itxn
    return(np.array(itxn_corr), itxn_features)

itxn_cluster, cluster_f = itxn_correlation(all_num, tmacc_id, cluster_id)
itxn_card, card_f = itxn_correlation(all_num_card, tmacc_id, card_id)
