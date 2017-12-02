# This is not a working piece of code!
#cog_category
with open("/home/hermuba/ecoli.cog.list") as f:
    for line in f:
        line = line.replace('\n', '')
        genome_id = line.split('\t')[0]
        protein_id = line.split('\t')[1]
        head = protein_id+'|'+genome_id
        if head in list(cluster_detail['representing gene header']):
            index = cluster_detail.loc[cluster_detail['representing gene header'] == head].index
            cluster_detail.loc[index, 'cog'] = line.split('\t')[2]

# add on card annotation (each member)
def card_in_cluster(cluster_name):
    count = 0
    members = cluster_detail.loc[cluster_name, 'member'].split(',')[1:] # the first element is ''
    for mem in members:
        genome_id = mem.split('|')[1]
        protein_id = mem.split('|')[0]

        df = pd.read_pickle("../../cdhitResult/card_detail_df/"+genome_id)
        if protein_id in df.index:
            count = count + 1

    return(count, count/len(members))
for clu in cluster_detail.index:
    count, portion = card_in_cluster(clu)
    cluster_detail.loc[clu, "card_portion"] = portion
    cluster_detail.loc[clu, "card_count"] = count

# add "prevalance" to cluster_detail
cluster_detail['prevalance'] = df.mean() # __% genome has that gene
