
import pandas as pd

def anno_significant(scoary_file):
    df = pd.read_csv(scoary_file)
    card = pd.read_pickle("/home/hermuba/data/genome/prokka/gff/group_with_card_df")

    return(df.merge(card[['best_ARO', 'group']], how = 'left', left_on = "Gene", right_on = "group"))

from os import listdir
from os.path import isfile, join
mypath = "/home/hermuba/data/genome/prokka/gff/scoary_result/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
with open(mypath+'card_identified', 'w') as g:
    for f in onlyfiles:
        d = anno_significant(mypath + f)
        identified_card = d.loc[d['best_ARO'].notnull()]['best_ARO']
        g.write(f+'\n')
        g.write(str(list(identified_card))+'\n')
