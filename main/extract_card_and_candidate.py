# combined network
net = '/home/hermuba/data0118/network1122/combined_baye'

# output file:
output_net = '/home/hermuba/data0118/network1122/card_lls'

# annotations
import pandas as pd
gold_anno = pd.read_csv('/home/hermuba/data0118/network1122/gold_anno.csv', header = 0, index_col = 0)

# find genes with card annotation!
card = gold_anno.loc[gold_anno['is_card'] == True].index

# find interactions containing card genes
net_chunks = pd.read_csv(net, header = 0, chunksize = 10000)

# find card
def find_gene_subset(df, gene_id_set):

    # find the index
    first_por = df.loc[df['gene_one'].isin(gene_id_set)].index
    sec_por = df.loc[df['gene_two'].isin(gene_id_set)].index

    # union the index
    all_indices = list(set(first_por).union(set(sec_por)))

    return(df.loc[all_indices])


# iterate by chunk
for n in net_chunks:
    d = find_gene_subset(n, card)

    print(d.shape)

    with open(output_net, 'a') as f:
        d.to_csv(f, header = False)
