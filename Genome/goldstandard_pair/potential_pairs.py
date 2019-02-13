# input

import pandas as pd
df = pd.read_pickle('/home/hermuba/data0118/goldstandard/node_anno_df')

# all possible pairs

from itertools import combinations

all_com = combinations(list(df.index), 2)

# write to csv
with open('/home/hermuba/data0118/all_possible_comb','a') as f:
    for com in all_com:
        f.write(','.join(list(com))+ '\n')
