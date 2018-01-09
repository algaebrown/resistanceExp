# readfile
multiple_sdf = '/home/hermuba/data/drug/all_five_sdf.sdf'
csv = '/home/hermuba/data/drug/all_five.csv'
# import pybel
import pybel
import pandas as pd

df = pd.read_csv(csv, index_col = False)
df.shape
n = []
for molecule in pybel.readfile("sdf",multiple_sdf):
    name  = molecule.data['PATRIC_NAME_TAG']
    n.append(name)

df['chem_name'] = n
df.to_pickle('/home/hermuba/data/tmacc_df')
