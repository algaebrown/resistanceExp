import pandas as pd
import numpy as np
import os
import sys
ris_file = sys.argv[1] # phenotype pivot table
clstr_csv = sys.argv[2] #.clstr.csv
outf = sys.argv[3]

# output to scoary
trait_file = os.path.join(outf, 'scoary_trait.csv')
abs_file = = os.path.join(outf, 'gene_abs.Rtab')


# read files 
genotype = pd.read_csv(clstr_csv, index_col = 0, header = 0)
phenotype = pd.read_csv(ris_file, header = 0, dtype = str)
phenotype.set_index('genome_id', inplace = True)
print("files read")


# ==== generate trait table =====
matrix  = phenotype.loc[phenotype.index.isin(genotype.columns)]
print("selecting included genome")
# select antibiotic with abundant data
matrix = matrix.loc[:,matrix.count() > 50]
# scoary fails if data = 1
matrix.fillna('NA', inplace = True)
matrix.replace('0.0', '0', inplace = True)
matrix.replace('1.0', '1', inplace = True)

matrix.to_csv(trait_file, index_label = 'Name')
print("phenotype pivot table saved")

#======generate pangenome absence presence pattern======


# remove the last line of nan
pan = genotype.iloc[:-1, :]
pan = pan[matrix.index.tolist()] # only select genomes that has data
pan = pan.astype(int) # needs to be int
pan.to_csv(abs_file, index_label = 'Gene')
print("subset genomes with phenotype data")

#======run scoary======
os.system('scoary -g '+ abs_file + ' -t ' + trait_file + ' -s 2 --delimiter , --threads 16')
