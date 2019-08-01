
import pandas as pd
def parse_card(txt_file):
    '''
    a function to parse card output
    input: card RGI output .txt
    output: dataframe containing all hits
    '''
    df = pd.read_csv(txt_file, header = 0, sep = '\t')
    return(df)

def process_card(df):
    '''
    input: row = hit; column = card info
    ouput: row = each gene; index = gene_id; columns = 'BEST_Hit_ARO', 'ARO', 'ARO_name', 'Best_Hit_ARO_category', 'ARO_category'
    '''

    # filter by e-value cause it's the loose mode

    df = df.loc[df['Best_Hit_evalue']<0.00001] # e-value cutoff < 10^ -5

    # split the representing gene id
    df.set_index(df['ORF_ID'].str.split(' ', expand = True)[0])

    # drop old ORF ID
    df.drop('ORF_ID', axis = 1)

    return(df)


def extract_ARO(df):
    '''
    to extract ARO category from dataframe from `process_card`
    input: dataframe from process_card
    output: dataframe with ARO category as columns, genes as names.
    '''
    parsed_category = df['Best_Hit_ARO_category'].apply(lambda x: x.split('; '))
    flattened_list = list(set([y for x in parsed_category for y in x])) # unique categories

    # save to dataframe
    all_category = pd.DataFrame(index = df.index, columns = flattened_list)

    n = 0
    for p in parsed_category:
        i = df.index[n] # gene name
        all_category.loc[i, p] = True
        n += 1

    all_category.fillna(False, inplace = True)

    return(all_category)
