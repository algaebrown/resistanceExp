import pandas as pd

path = "/home/hermuba/data/ml_results/"
train_drug = ['meropenem','cefepime','ceftazidime' ,'gentamicin', 'ciprofloxacin','trimethoprim_sulfamethoxazole', 'ampicillin', 'cefazolin', 'ampicillin_sulbactam']

all_df = pd.DataFrame()
for i in train_drug:
    all_df = all_df.append(pd.read_pickle(path + i + "_ml_df"))

all_df.to_excel(path+'results.xlsx')
