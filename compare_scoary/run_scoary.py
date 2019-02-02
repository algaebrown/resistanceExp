ris_file = "/home/hermuba/data0118/annotated_RIS/anno_df"
pan_file = "/home/hermuba/data0118/cdhit/clstr/pangenome_df/Escherichia0.70.clstr.csv"
trait_file = '~/data0118/scoary/scoary_trait.csv'
abs_file = '~/data0118/scoary/gene_abs.Rtab'
#======generate trait file======

# ris dataframe: select only E.coli
import pandas as pd
ris = pd.read_pickle(ris_file)
ris_need = ris[['Genome ID', 'Antibiotic', 'Resistant Phenotype', 'Measurement Value', 'Species']]
ris_need = ris_need.loc[ris_need['Species'] == 'Escherichia']
# change to binary
to_binary={'Resistant': 1,
           'Susceptible': 0}
ris_need['Resistnat Phenotype'] = ris_need['Resistant Phenotype'].map(to_binary)

# construct the row = genome; column = trait table
genome = ris_need['Genome ID'].unique()
abx = ris_need['Antibiotic'].unique()
matrix = pd.DataFrame(columns = abx, index = genome)
import numpy as np
for index, row in ris_need.iterrows():
    if row['Resistant Phenotype'] == "Resistant":
        matrix.loc[row['Genome ID'], row['Antibiotic']] = 1
    elif type(row['Resistant Phenotype']) == str:
        matrix.loc[row['Genome ID'], row['Antibiotic']] = 0
    else:
        matrix.loc[row['Genome ID'], row['Antibiotic']] = 'NA'




# save trait file to csv
matrix.to_csv(trait_file)

#======generate pangenome absence presence pattern======
pan = pd.read_csv(pan_file, index_col = 0, header = 0)
import numpy as np
pan = pan.iloc[:-1, :]
pan = pan.astype(int).replace(0, np.nan)
pan.to_csv(abs_file, index_label = 'Gene')


#======run scoary======
import os
os.system('scoary -g '+ abs_file + ' -t ' + trait_file + ' -s 1 --delimiter ,')

# this script cannot work: pdist: 2 dimensional array required...= =
