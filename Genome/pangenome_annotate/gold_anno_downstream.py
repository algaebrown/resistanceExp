# This file is to process gold_anno annotations to interpret groups of protein, most popular resfam/domain/COG annotation
import pandas as pd
def count_cog(df):
    ''' count number of genes attributed to a specific COG annotation '''
    popular_cogs = df['cog_ID'].value_counts().to_frame(name='no_genes')
    
    # read cog names
    cog_names = pd.read_csv('/home/hermuba/bin/COGmapper/COGlist.txt', sep = '\t', index_col= 0, encoding = "ISO-8859-1")
    popular_cogs['name']= cog_names.loc[popular_cogs.index, 'name']
    
    return popular_cogs.sort_values('no_genes')

def count_domain(df):
    ''' count domain occurence '''
    all_domain = set()
    _ = [all_domain.update(i) for i in df['domain'] if type(i)!= float]
    
    domain_metadata = pd.read_csv('~/data0118/entry.list', sep = '\t', index_col = 0, header = 0)
    domain_metadata = domain_metadata.loc[list(all_domain)]
    
    domain_metadata['no_genes'] = 0
    for i in df['domain']:
        if type(i) != float:
            family = list(i)
        
            domain_metadata.loc[family, 'no_genes'] = domain_metadata.loc[family, 'no_genes'] + 1
    return domain_metadata.sort_values(by = 'no_genes', ascending = False)


