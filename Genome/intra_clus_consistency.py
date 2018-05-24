# Within a gene cluster, how many components are there?
# define components = ARO; pfam...
import pandas as pd
cluster_df_path = "/home/hermuba/data0118/cdhit/clstr/cluster_detail/"
comp_df_path = "/home/hermuba/data0118/pfam/df/"
def read_cluster(cluster_name):

    # this df contains cluster representing genes and all of its members
    cluster_df = pd.read_csv("/home/hermuba/data0118/cdhit/clstr/cluster_detail/"+cluster_name+'.clstr.tab', sep = '\t')

    return(cluster_df)
def split_genome(s):
    """
    because the way we store genome information as protein_name|genome_id, this parser will find the genome id for us
    input: 562.22913.con.0045_7|562.22913
    output: 562.22913
    """
    return(s.split('|')[1])

def extract_card_clus(filename):
    """
    the case with card is special: NOT every gene has CARD annotation. To save computational resource, we will retain only clusters with CARD annotations for comparison
    input: filename = SPECIES + THRESHOLD
    output: df with representing genes with CARD annotations
    """
    rep_with_card = pd.read_pickle("/home/hermuba/data0118/cdhit/card/"+ filename+"_df").index
    clus_detail = read_cluster(filename)
    combined_detail = clus_detail.loc[clus_detail['representing_gene'].isin(rep_with_card)]
    combined_detail['rep_genome'] = combined_detail['representing_gene'].map(split_genome)
    return(combined_detail)

import os
def all_available_components(comp_df_path):
    onlyfiles = [f.replace('.faa', '') for f in os.listdir(comp_df_path) if os.path.isfile(os.path.join(comp_df_path, f))]
    return(onlyfiles)

card_path = '/home/hermuba/data0118/predicted_genes/card/'
def find_card(genome_id, gene_name):
    """
    to get card annotation from file
    input: genome id and gene name
    output: card ARO
    """
    card = pd.read_pickle(card_path + genome_id)
    return(card.loc[gene_name, 'ARO_name'])
pfam_path = "/home/hermuba/data0118/pfam/df/"
def find_pfam(genome_id, gene_name):
    """
    to get pfam annotation from file
    input: genome id and gene name
    output: pfam name
    """
    pfam = pd.read_pickle(pfam_path + genome_id + '.faa')
    all_hmm = pfam.loc[pfam['seq id'] == gene_name]

    return(all_hmm['hmm name'].drop_duplicates().to_string(index = False))
    #return(pfam.loc[pfam['seq id'] == gene_name]['hmm name'].to_string(index = False))

def find_mem_comp(df, comp_path, comp_type):
    """
    find all aro (if exist) within a cluster, if the member belongs to the 100 genome
    input:
    1. df with cluster id and its member
    2. comp_path: folder where comp_df is stored
    3. comp_type: card or pfam
    output: list of list
    [Cluster_1_list, Cluster_2_list...]
    Cluster_1_list = [ARO_for_member1, ARO_for_member2]
    """
    comps = []
    for clus in df['members']:
        clus_mem = clus.split(',')[1:] # all members of a cluster
        all_comps = []
        for mem in clus_mem:
            #print(mem)
            gene_name = mem.split('|')[0]
            genome_id = mem.split('|')[1]
            onlyfiles = all_available_components(comp_path)
            if genome_id in onlyfiles:
                try:
                    if comp_type == 'card':
                        c = find_card(genome_id, gene_name)
                    if comp_type == 'pfam':
                        c = find_pfam(genome_id, gene_name)
                        all_comps.append(c)

                except KeyError:
                    #print(gene_name, genome_id, 'card annotation not found')
                    do_nothing = 0
        comps.append(all_comps)
    return(comps)

def consistency(l):
    df = pd.DataFrame(columns = ['members', 'no_members', 'cluster_size'])
    index = 0
    for clus in l:
        if len(clus)>0:
            index = index + 1
            members = set(clus)
            how_many_kind = len(members)
            no_member = len(clus)
            df.loc[index] =[members, how_many_kind, no_member]
    return(df)
