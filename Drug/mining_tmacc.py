import pandas as pd

# import data
df = pd.read_pickle('/home/hermuba/data/drug/tmacc_df')
# ACTIVITY does not make any sense
df.drop('ACTIVITY', axis=1, inplace=True)
# set antibiotic name as index
df.set_index('chem_name', drop=True, append=False, inplace=True)
print(df.shape)
# there are 81 cols with std = 0, drop them
df.drop(columns = df.std().loc[df.std() == 0].index, inplace = True)
print(df.shape)

# there are some nans, all of them in 'Maximum:ScaledAtomPartialPositiveCharge:ScaledAtomPartialPositiveCharge:0'
print(df.isnull().any(axis = 1), df.isnull().any(axis = 0))

# normalization: proven to be better than those not normalized
df = df.fillna(0)
norm_df = df.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

# correlation
corr = norm_df.corr()
identical = []
for index, row in corr.iterrows():
    the_set = set(row.loc[row == 1].index)
    print(len(the_set))
    if len(the_set) > 1 and (the_set not in identical):
        identical.append(the_set)

# save to repeat_tmacc
with open('repeat_tmacc', 'w') as f:
    for i in identical:
        f.write(str(i))

# remove the repeated tmacc
norm_df = norm_df.T.drop_duplicates().T
norm_df.to_pickle("/home/hermuba/data/drug/norm_tmacc")

# pca
import numpy as np
from sklearn.decomposition import PCA

pca = PCA(n_components = 30)
pca.fit(norm_df)
pc = pca.fit_transform(norm_df, norm_df.index)
tmacc_pca = pd.DataFrame(pc, index = norm_df.index)
tmacc_pca.to_pickle("/home/hermuba/data/drug/pca_tmacc")
