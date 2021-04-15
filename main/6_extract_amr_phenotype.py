# download amr phenotypes here
# ftp://ftp.patricbrc.org/RELEASE_NOTES/PATRIC_genomes_AMR.txt

import pandas as pd
import numpy as np
from optparse import OptionParser
parser = OptionParser()

parser.add_option("-a", "--amr", dest="amr",
                  help="PATRIC AMR file, download from ftp://ftp.patricbrc.org/RELEASE_NOTES/PATRIC_genomes_AMR.txt", default = '/nas2/users/hermuba/amr/PATRIC_genomes_AMR.txt')
parser.add_option("-g", "--stat", dest="stat",
                  help="genome_statistics")
parser.add_option("-o", "--out", dest="outf",
                  help="output folder and amr.pivot.csv")
(options, args) = parser.parse_args()


amr = pd.read_csv(args.amr, sep = '\t', dtype = {'genome_id': str})
genome_stat = pd.read_csv(args.stat, dtype = {'Unnamed: 0': str})
genome_stat.set_index('Unnamed: 0', inplace = True)
included_ids = genome_stat.loc[genome_stat['include']].index

def filtering(df):
    """ Remove data duplicates, without y, wrong lab (into train)

    >>> filtering(df)

    """
    # remove duplicates: same Genome ID and same drug
    df.drop_duplicates(subset = ['genome_id', 'antibiotic'], inplace = True)
    df.dropna(subset = ['resistant_phenotype', 'laboratory_typing_method'], inplace = True)

    df.reset_index(inplace = True)
    

    

    return df


def process_drug(df):
    ''' do a bit of data cleaning '''
    # make all not capital
    df['antibiotic'] = df['antibiotic'].str.lower()

    # deal with space, '-', '/'
    df['antibiotic'] = df['antibiotic'].str.replace('/', '-')

    # clavunate
    df['antibiotic'] = df['antibiotic'].str.replace('clavulanic acid', 'clavulanate')
        
    return df





# select only genomes included
amr = amr.loc[amr['genome_id'].isin(included_ids)]

# filter by data quality
amr = filtering(amr)

# unify antibiotic name
amr = process_drug(amr)

# save
amr.to_csv(os.path.join(arg.outf, 'amr.csv'), index = False)

# to pivot
amr_pivot = amr.pivot(index = 'genome_id', columns = 'antibiotic', values = 'resistant_phenotype')
from collections import defaultdict
binary_dict = defaultdict(lambda: np.nan, {'Resistant':1, 'Susceptible': 0})
amr_pivot = amr_pivot.applymap(lambda x: binary_dict[x])
amr_pivot.to_csv(os.path.join(arg.outf, 'amr.pivot.csv'), index = True)



