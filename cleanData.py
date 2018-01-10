# input: patric AMR data
# output: genome list(unique); drug list(unique);clean data(with correct lab methods); test data(not with correct lab methods)

# import
import pandas as pd
import logging
import doctest

# read file
excel_path = '../data0118/patric_original/'
test = pd.read_pickle("test/test_data")
# logging
logging.basicConfig(filename = excel_path + 'cleanData.log', level = logging.DEBUG)

# strictly assign data type
c = {'Genome ID' : str, 'Taxon ID' : str, 'Genome Name': str, 'Antibiotic': str, 'Resistant Phenotype': str, 'Measurement Value': str, 'Testing Standard Year': int}

# read into dataframe
entero_df = pd.read_excel(excel_path + 'PATRIC_genome_amr_escherichia_20180108.xlsx', converters = c)
acineto_df = pd.read_excel(excel_path + 'PATRIC_genome_amr_acineto_20180108.xlsx', converters = c)
pseudo_df = pd.read_excel(excel_path + 'PATRIC_genome_amr_pseudo_20180108.xlsx',converters = c)
old_entero_df = pd.read_excel(excel_path + 'PATRIC_genome_amr_20170708.xlsx', converters = c)

# combine to one df
frames = [entero_df, acineto_df, pseudo_df, old_entero_df]
total_df = pd.concat(frames, ignore_index = True)
print('All columns: '+ total_df.columns.values)
print('All lab methods: ' ,total_df['Laboratory Typing Method'].unique())

# filter
def filtering(df):
    """ Remove data duplicates, without y, wrong lab (into train)

    >>> filtering(df)

    """
    # remove duplicates: same Genome ID and same drug
    df.drop_duplicates(subset = ['Genome ID', 'Antibiotic', 'Resistant Phenotype'], inplace = True)
    print(df.shape)
    # empty Resistant Phenotype AND Measurement Value: totally useless
    no_pheno = df.loc[df['Resistant Phenotype'].isnull()]
    useless = no_pheno.loc[no_pheno['Measurement'].isnull()].index
    print(useless)
    df.drop(labels = useless, axis = 0, inplace = True)

    df.reset_index(inplace = True)
    # Labortory Typing Method 'disk diffusion','breakpoint', 'compuational prediction': go to test set (because will mess up with measurement)

    rm = ['Computational Prediction', 'breakpoint', 'disk diffusion']
    wrong_lab = df.loc[df['Laboratory Typing Method'].isin(rm)].index
    logging.info('removing lab method from train'+str(rm))
    print(wrong_lab)

    test_set = df.iloc[wrong_lab, :] #leave for last validation
    train_set = df.drop(index = test_set.index)

    return(test_set, train_set, df)


def process_drug(df):
    # make all not capital
    df['Antibiotic'] = df['Antibiotic'].str.lower()

    # deal with space, '-', '/'
    df['Antibiotic'] = df['Antibiotic'].str.replace('/', '-')

    # clavunate
    df['Antibiotic'] = df['Antibiotic'].str.replace('clavulanic acid', 'clavunate')
    to_txt(df['Antibiotic'].unique(), 'drug')
    return(df)

sps_dict = {'Pseudomonas': 'Pseudomonas aeruginosa',
            'Acinetobacter': 'Acinetobacter spp.',
            'Klebsiella': 'Klebsiella',
            'Escherichia': 'Escherichia',
            'Salmonella': 'Salmonella',
            'Shigella': 'Shigella',
            'Citrobacter': 'Citrobacter',
            'Enterobacter': 'Enterobacter'}

def rm_annotate_sps(df):
    sps = pd.DataFrame()
    # remove unwanted species
    def sps(g_name):
        for label in sps_dict.keys():
            if label in g_name:
                return(sps_dict[label])
    df['Species'] = df['Genome Name'].apply(lambda x: sps(x))
    # drop unwanted species
    unwanted =  df.loc[df['Species'].isnull()].index
    df.drop(index = unwanted, inplace = True)
    return(df)

def to_txt(series, name):
        with open('../data0118/genomeList/' + name, 'w') as f:
            for element in series:
                f.write(element + '\n')

def genome_list(df):
    # species-wise

    for sps in df['Species'].unique():
        genome_list = df.loc[df['Species'] == sps]['Genome ID'].unique()
        to_txt(genome_list, sps)
    # altogether
    genome_list = df['Genome ID'].unique()
    to_txt(genome_list, 'all')

def data_type_conversion(df):
    cat_dict = {}

    # assign to right data type
    for col in ['Resistant Phenotype', 'Laboratory Typing Method', 'Testing Standard', 'Antibiotic', 'Species']:
        cat_dict[col] = 'category'
    for col in ['Taxon ID', 'Genome ID']:
        cat_dict[col] = 'object'


    cat_dict["Measurement Value"] = 'str'

    df.astype(cat_dict, copy = False)
    return(df)

test, train, total = filtering(total_df)
name = ['test_data', 'clean_data', 'total_data']
dfs = [test, train, total]
for i in range(3):
    s = rm_annotate_sps(process_drug(dfs[i]))
    genome_list(s)
    df = data_type_conversion(s)
    df.to_pickle("../data0118/"+name[i])
