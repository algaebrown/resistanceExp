card_path = "/home/hermuba/resistanceExp/EcoliGenomes/cdhitResult/ec0913_card.txt"

with open(card_path) as f:
    all_lines = f.readlines()

import pandas as pd
card_detail = pd.DataFrame(columns = ['ARO', 'ARO_name', 'ARO_group', 'snp', 'cut_off'])

# parsing
header = all_lines[0].split('\t') # len = 25
for i in range(1, len(all_lines)):
    attr = all_lines[i].split('\t')

    gene_header = attr[0].split(' ')[0] # JMUY01000005_592|1438670.3
    cut_off = attr[5] # strict
    ARO = attr[10] # can be more than one
    ARO_name = attr[11] # string
    snp = attr[13] # can be 'n/a'
    ARO_group = attr[15]

    card_detail.loc[gene_header] = pd.Series({'ARO':ARO, 'ARO_name':ARO_name, 'ARO_group':ARO_group, 'snp':snp, 'cut_off': cut_off})
