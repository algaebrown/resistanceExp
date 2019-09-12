ris_file = "/home/hermuba/data0118/annotated_RIS/RIS_pivot_ecoli.csv"
pan_file = "/home/hermuba/data0118/cdhit/clstr/pangenome_df/Escherichia0.70rm_plasmid.clstr.csv"
trait_file = '~/data0118/scoary/scoary_trait.csv'
abs_file = '~/data0118/scoary/gene_abs.Rtab'
#======generate trait file======

# ris dataframe: select only E.coli
import pandas as pd
pan = pd.read_csv(pan_file, index_col = 0, header = 0)
ris = pd.read_csv(ris_file, header = 0, dtype = str)
ris.set_index('Genome ID', inplace = True)
print("files read")

# select included genome
matrix  = ris.loc[ris.index.isin(pan.columns)]
print("selecting included genome")
# fill na
# scoary fails if data = 1
matrix = matrix.loc[:,matrix.count() > 50]
matrix.fillna('NA', inplace = True)
matrix.replace('0.0', '0', inplace = True)
matrix.replace('1.0', '1', inplace = True)






matrix.to_csv(trait_file, index_label = 'Name')
print("phenotype pivot table saved")

#======generate pangenome absence presence pattern======

import numpy as np
# remove the last line of nan
pan = pan.iloc[:-1, :]

pan = pan[matrix.index.tolist()]
pan = pan.astype(int) # needs to be int
pan.to_csv(abs_file, index_label = 'Gene')
print("subset genomes with phenotype data")

#======run scoary======
import os
os.system('scoary -g '+ abs_file + ' -t ' + trait_file + ' -s 2 --delimiter , --threads 16')
