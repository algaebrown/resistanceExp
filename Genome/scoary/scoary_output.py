import pandas as pd

# detail parses any CARD output(.txt) and turn it into a dataframe
def detail(p):
    with open(p) as f:
        all_lines = f.readlines()


    card_detail = pd.DataFrame(columns = ['ARO', 'ARO_name', 'ARO_group', 'snp', 'cut_off', 'best_ARO', 'best_identity'])

    # parsing
    header = all_lines[0].split('\t') # len = 25
    for i in range(1, len(all_lines)):
        attr = all_lines[i].split('\t')

        gene_header = attr[0].split(' ')[0][:-2]
        # card add something to each gene header
        print(gene_header)
        cut_off = attr[5] # strict
        ARO = attr[10] # can be more than one
        best_ARO = attr[8]
        best_identity = attr[9]
        ARO_name = attr[11] # string
        snp = attr[13] # can be 'n/a'
        ARO_group = attr[15]

        card_detail.loc[gene_header] = pd.Series({'ARO':ARO, 'ARO_name':ARO_name, 'ARO_group':ARO_group, 'snp':snp, 'cut_off': cut_off, 'best_ARO': best_ARO, 'best_identity' : best_identity})
    return(card_detail)

# parse roary file, output: df with group XXX, gene_header
def parse_roary(filename):
    headers = []
    groups = []
    with open(filename) as f:
        for line in f:
            if '>' in line:
                headers.append(line.replace('>', '').replace('\n', '').split(' ')[0])
                groups.append(line.replace('>', '').replace('\n', '').split(' ')[1])
    df = pd.DataFrame()
    df['gene_header'] = headers
    df['group'] = groups

    return(df)

# parse group number along with gene header
roary_file = "/home/hermuba/data/genome/prokka/gff/pan_genome_reference.fa"
roary_with_card = "/home/hermuba/data/genome/prokka/gff/pan_genome_reference_card.fa.txt"

df = parse_roary(roary_file)
card = detail(roary_with_card)
# merge df
merged = card.merge(df, left_index = True, right_on = 'gene_header')

merged.to_pickle("/home/hermuba/data/genome/prokka/gff/group_with_card_df")
