
import pandas as pd
def parse_card(txt_file):
    '''
    a function to parse card output
    input: card RGI output .txt
    output: dataframe containing all hits
    '''
    df = pd.read_csv(txt_file, header = 0, sep = '\t')

    # split the representing gene id
    df.set_index(df['ORF_ID'].str.split(' ', expand = True)[0], inplace = True)
    # drop old ORF ID
    df.drop('ORF_ID', axis = 1, inplace = True)

    return df



def extract_ARO(df, category_column = 'Drug Class'):
    '''
    to extract ARO category from dataframe from `process_card`
    input: dataframe from process_card
    output: dataframe with ARO category as columns, genes as names.
    '''
    parsed_category = df[category_column].apply(lambda x: x.split('; '))
    flattened_list = list(set([y for x in parsed_category for y in x])) # unique categories

    # save to dataframe
    all_category = pd.DataFrame(index = df.index, columns = flattened_list)

    n = 0
    for p in parsed_category:
        i = df.index[n] # gene name
        all_category.loc[i, p] = True
        n += 1

    all_category.fillna(False, inplace = True)

    return all_category
