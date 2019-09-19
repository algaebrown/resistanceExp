# putative genes with of each antibiotics (either from scoary, from network candidates, from significant genes), plot heatmap and compare to current knowledge(resfam, CARD)

import pandas as pd
import numpy as np
import math
def preprocess_odds_df(df):
    '''
    to preprocess_odds_ratio_df
    input: df with odds ratio for each gene for each abx

    columns = genes
    index = abx
    '''

    # select only genes with data
    df = df.loc[:, df.count()>1]

    # replace inf and -inf
    maximum = df.max().max()
    minimum = df.min().min()

    df = df.replace(np.inf, maximum*10).replace(-np.inf, minimum*0.1).fillna(1)
    return(df)

def log_odds(df):
    '''
    do log10 transform of preprocessed df
    '''
    return(df.applymap(math.log10))

#======= PREPROCESSING ABX ANNOTATION =======#
# convert boolean (True False annotation) into one gene per color annotation
def bool_categorize(df):
        x = df.stack()
        return(pd.Series(pd.Categorical(x[x!=0].index.get_level_values(1)), index = x[x!=0].index.get_level_values(0)))

def card(file = '/home/hermuba/data0118/Escherichia0.70rm_plasmid_card.csv'):
    '''
    Turn CARD annotation into abx-specific info and efflux pump
    '''

    card = pd.read_csv(file, index_col = 0)

    #===== extract antibiotic-specific resistant genes =====#
    abx_spec = card.loc[:, card.columns.str.contains('determinant')]

    # replace column names
    def replace_col_names(s):
        s = s.replace('determinant of ','').replace(' resistance', '').replace('resistance to', '').lower()
        return(s)

    abx_spec.rename(columns = replace_col_names, inplace = True)

    # make into a series of categorical data

    abx_cat = bool_categorize(abx_spec)

    #==== extract efflux-pump related information=====#
    efflux_pump = card.loc[:, 'efflux pump complex or subunit conferring antibiotic resistance']

    return(abx_cat , efflux_pump)

def resfam(abx_file = '/home/hermuba/data0118/resfam_anno_abx.csv', mech_file = '/home/hermuba/data0118/resfam_anno.csv'):

    resfam = pd.read_csv(mech_file, index_col = 0)
    resfam_mech = bool_categorize(resfam)

    abx = pd.read_csv(abx_file, index_col = 0)
    resfam_abx = bool_categorize(abx)

    return(resfam_mech, resfam_abx)

#===================== DRUG category ===============================#
def drug(file = '/home/hermuba/data0118/drug_category'):
    drug_df = pd.read_pickle(file)


    return(drug_df)

def drug_legend(drug_df):
    lut_keys = drug_df[['drug_color', 'category']].drop_duplicates()

    import matplotlib.patches as mpatches
    legend = [mpatches.Patch(color = lut_keys.loc[i, 'drug_color'], label = lut_keys.loc[i, 'category']) for i in lut_keys.index]

    return(legend)




#====================== COLORMAP for them ===========================#
