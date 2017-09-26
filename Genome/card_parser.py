# filelist
list_path = "../../data/allgenomelist.txt"
with open(list_path) as f:
    genome_list = f.read().splitlines()

# path to card anno
card_path = "../../data/genePredicted/resGeneTxt/"

from multiprocessing import Pool

# parsing card txt file
def card_txt_parser(ID):
    with open(card_path + ID + '.txt') as card:
        listOfARO = []
        for lines in card:
            x = lines.split("\t")
            if len(x[10])>3:
                if ',' in x[10]:
                    aroID = x[10].split(',')
                    aroID = aroID[0]
                    #print(aroID)
                else: aroID = x[10]
                num = int(aroID[4:])
                listOfARO.append(num)

    return(listOfARO)





import pandas as pd
df = pd.DataFrame()

for index in range(len(genome_list)):
    aro_list = card_txt_parser(genome_list[index])
    for aro in aro_list:
        df.loc[genome_list[index], aro] = True

df = df.fillna(False)
df.to_pickle('../../data/aro_pattern_df')
