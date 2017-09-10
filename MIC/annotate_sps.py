from micToris import identify_sps

import pandas as pd
df = pd.read_pickle("../../data/anno_df")

genus = ['Klebsiella', 'Escherichia', 'Salmonella', 'Shigella', 'Citrobacter', 'Enterobacter']
for index, row in df.iterrows():
    sps = identify_sps(row)
    if sps == "Enterobacteriae":
        for g in genus:
            if g in row["Genome Name"]:
                df.ix[index, 'Species'] = g
                print(g, df.ix[index, "Genome Name"])
    else:
        df.ix[index, 'Species'] = sps
df.to_pickle("../../data/anno_sps_df")
