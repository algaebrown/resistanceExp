
card_path = '/home/hermuba/data/genePredicted/resGeneTxt'

with open("/home/hermuba/data/genomeList/ECgenome.txt") as f:
    genome_list = f.read().splitlines()
import pandas as pd
def detail(p):
    with open(p) as f:
        all_lines = f.readlines()


    card_detail = pd.DataFrame(columns = ['ARO', 'ARO_name', 'ARO_group', 'snp', 'cut_off', 'best_ARO', 'best_identity'])

    # parsing
    header = all_lines[0].split('\t') # len = 25
    for i in range(1, len(all_lines)):
        attr = all_lines[i].split('\t')

        gene_header = attr[0].split(' ')[0] # JMUY01000005_592|1438670.3
        cut_off = attr[5] # strict
        ARO = attr[10] # can be more than one
        best_ARO = attr[8]
        best_identity = attr[9]
        ARO_name = attr[11] # string
        snp = attr[13] # can be 'n/a'
        ARO_group = attr[15]

        card_detail.loc[gene_header] = pd.Series({'ARO':ARO, 'ARO_name':ARO_name, 'ARO_group':ARO_group, 'snp':snp, 'cut_off': cut_off, 'best_ARO': best_ARO, 'best_identity' : best_identity})
    return(card_detail)

for genome in genome_list:
    card_detail = detail(card_path +'/'+ genome + '.txt')
    card_detail.to_pickle('/home/hermuba/data/genePredicted/card_detail_df/'+genome)
    print(card_detail.shape)
