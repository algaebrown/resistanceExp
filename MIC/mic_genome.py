# import annotated, cleaned phenotype of E.coli

import pandas as pd
anno_df = pd.read_pickle('/home/hermuba/data0118/annotated_RIS/anno_df')

selected = anno_df.loc[anno_df['Species'] == 'Escherichia']
selected['mapped_pheno'] = selected['Resistant Phenotype'].map({'Resistant':1, 'Susceptible':0})

pivot_t = pd.pivot_table(selected, values = 'mapped_pheno', index = 'Genome ID', columns = 'Antibiotic')
