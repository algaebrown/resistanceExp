import pandas as pd
df = pd.read_pickle('/home/hermuba/data0118/goldstandard/ec_rmplasmid_node_anno_df')

domain = df['domain'].dropna()
total_set = set()
for protein in domain:
    total_set = total_set.union(protein)

# True/False for domain presence abscence
outfile = '/home/hermuba/data0118/domain_abs_rm_plasmid'


for i, protein in enumerate(domain):
    domain_df = pd.DataFrame(columns = list(total_set))
    for each_domain in protein:
        domain_df.loc[domain.index[i], each_domain] = 1
        domain_df = domain_df.fillna(0)

    if i == 0:
        with open(outfile, 'w') as f:
            domain_df.to_csv(f, header = True)
    else:
        with open(outfile, 'a') as f:
            domain_df.to_csv(f, header = False)
    print('doing ' + str(i) + ' out of ' + str(len(domain)))

# calculate weight
