
import pandas as pd

def anno_significant(scoary_file):
    df = pd.read_csv(scoary_file)
    card = pd.read_pickle("/home/hermuba/data/genome/prokka/gff/group_with_card_df")

    return(df.merge(card[['best_ARO', 'group']], how = 'left', left_on = "Gene", right_on = "group"))


from os import listdir
from os.path import isfile, join
# to generate txt containing scoary genes that has CARD annotation
mypath = "/home/hermuba/data/genome/prokka/gff/scoary_result/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.remove('card_identified')
with open(mypath+'card_identified', 'w') as g:
    for f in onlyfiles:
        d = anno_significant(mypath + f)
        identified_card = d.loc[d['best_ARO'].notnull()]['best_ARO']
        g.write(f+'\n')
        g.write(str(list(identified_card))+'\n')

# map abs pattern into binary
abs_file = pd.read_csv(mypath + 'gene_presence_absence.csv')
abs_file.set_index('Gene', inplace = True)
abs_file.drop(columns = abs_file.columns[:-59], inplace = True) # keep only genomes
binary_abs = abs_file.applymap(lambda x: 1 if type(x) == str else 0)
binary_abs = binary_abs.transpose()



# a function to get a list of CARD-scoary genes
# input: path to scoary drug.csv file
# output: list of drug with CARD annotation absence-presence pattern (group name)
def scoary_abs(f):
    d = anno_significant(mypath + f)
    identified_card = list(d.loc[d['best_ARO'].notnull()]['group'])
    if len(identified_card) > 0:
        isolated_df = binary_abs[identified_card]
        isolated_df.to_csv(mypath+'tab_card_scoary/'+f.split('_')[0]+'.tsv', sep = '\t')
        print(f, isolated_df.shape)
for f in onlyfiles:
    scoary_abs(f)
def scoary_abs_full(f):
    d = anno_significant(mypath + f)
    all_groups = d['Gene']
    if len(identified_card) > 0:
        isolated_df = binary_abs[all_groups]
        print(f, isolated_df.shape)
        isolated_df.to_csv(mypath+'tab_all_scoary/'+f.split('_')[0]+'.tsv', sep = '\t')
for f in onlyfiles:
    scoary_abs_full(f)
