# import
import pandas as pd

# read file
excel_path = '../data/'
# strictly assign data type
c = {'Genome ID' : str, 'Taxon ID' : str, 'Genome Name': str, 'Antibiotic': str, 'Resistant Phenotype': str, 'Measurement Value': str, 'Testing Standard Year': int}
entero_df = pd.read_excel(excel_path + 'entero.xlsx', converters = c)
acineto_df = pd.read_excel(excel_path + 'acineto.xlsx', converters = c)
pseudo_df = pd.read_excel(excel_path + 'pseudo.xlsx',converters = c)

# combine to one df
frames = [entero_df, acineto_df, pseudo_df]
total_df = pd.concat(frames)
print(total_df.columns.values)

rm = ['Computational Prediction', 'breakpoint', 'disk diffusion']

# remove computational prediction, breakpoint, disk diffusion
# sams contained only interpreted RIS by CLSI 2008
# leave it in but need furthur processing
rm_df = total_df.loc[~total_df['Laboratory Typing Method'].isin(rm)]

rm_sps = ['Hafnia alvei', 'Leclercia', 'Lelliottia']
# count species
# Citrobacter sp
# Enterobacter sp
# Escherichia coli
# Hafnia alvei only 1
# Klebsiella pneumoniae, some oxytoca
# Kluyvera sp
# Leclercia
# Lelliottia
# Salmonella enterica
# pseudomonas is clean and abundant (3067( and so is Acineto (5914)

# assign to right data type
for col in ['Resistant Phenotype', 'Laboratory Typing Method', 'Testing Standard', 'Antibiotic']:
    rm_df[col] = rm_df[col].astype('category')

for col in ['Taxon ID', 'Genome ID']:
    rm_df[col] = rm_df[col].astype('object')
rm_df["Measurement Value"] = rm_df["Measurement Value"].astype('str')
# reset index
rm_df.reset_index(inplace = True)

# save
rm_df.to_pickle("../data/clean_df")
