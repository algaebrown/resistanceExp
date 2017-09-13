# readfile

cdhit_result = '../../data/genePredicted/cdhit/ec0913.clstr'
f = open(cdhit_result)

# create dataframe
import pandas as pd
df = pd.DataFrame()

for line in f:
    if line[0] == '>':
        columnName = line.rstrip()[1:]
    else:
        ID = line.split('|')[1].split('...')[0]
        df.loc[ID, columnName] = True
df.fillna(False)
df.to_pickle("../../data/genePredicted/cdhit/ec0913_df")
f.close()
