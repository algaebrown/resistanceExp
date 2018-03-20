
#======generate trait file======

# ris dataframe: select only E.coli
import pandas as pd
ris = pd.read_pickle("/home/hermuba/data/annotated_RIS/anno_sps_df")
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
matrix.to_csv('~/data/genome/scoary_trait.csv')

#======generate pangenome absence presence pattern======
pan = pd.read_pickle("/home/hermuba/data/genePredicted/cdhit/ec0102_df")
pan.to_csv('~/data/genePredicted/cdhit/ec0102.csv')

#======mimicking roary output======
import numpy as np
roary = pan.transpose().astype(int).replace(0, np.nan)
roary.to_csv('~/data/roary.csv')
#======run scoary======
import os
os.system('scoary -g ~/data/genePredicted/cdhit/ec0102.csv -t ~/data/roary.csv')

# this script cannot work: pdist: 2 dimensional array required...= =
