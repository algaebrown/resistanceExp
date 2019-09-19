import pandas as pd
import numpy as np
clsi = pd.read_excel("/home/hermuba/data/annotated_RIS/CLSI_m100_breakpoint.xlsx")
category = clsi[['category', 'drug']]
category = category.drop_duplicates(subset = 'drug')
order = ['penicillins', 'b_lactam_inhibitor', 'cephems', 'monobactams', 'carbapenems', 'lipopeptides', 'phenicols', 'macrolides', 'aminoglycosides', 'tetracyclines', 'quinolones', 'folate_path','nitrofurans', 'fosfomycins', 'licosamide', 'pleuromutilin']

all_drug = ['ertapenem', 'cephalexin', 'clindamycin', 'polymyxin b', 'tilmicosin','tazobactam', 'imipenem', 'cefoperazone', 'sulbactam', 'doripenem','cefazolin', 'piperacillin', 'ceftazidime', 'timentin', 'trimethoprim','tigecycline', 'chloramphenicol', 'ceftriaxone', 'cefuroxime','amikacin', 'levofloxacin', 'sulfisoxazole', 'azithromycin','cefotaxime', 'danofloxacin', 'sulfamethoxazole', 'enrofloxacin','kanamycin', 'colistin', 'ticarcillin', 'doxycycline', 'gentamicin','cefotetan', 'fosfomycin', 'sulfadimethoxine', 'oxytetracycline','minocycline', 'cephalothin', 'ciprofloxacin', 'florfenicol','nalidixic acid', 'ceftiofur', 'clavulanic acid', 'tetracycline','tiamulin', 'neomycin', 'aztreonam', 'ampicillin', 'meropenem','tylosin', 'spectinomycin', 'nitrofurantoin', 'chlortetracycline','cefepime', 'streptomycin', 'cefoxitin', 'amoxicillin', 'tobramycin','norfloxacin', 'moxifloxacin', 'amoxicillin-clavunate', 'trimethoprim-sulfamethoxazole','cefalotin']

# ADD MISSING:

missing = list(set(all_drug)-set(category['drug']))
missing.sort()
cat = ['penicillins',
       'b_lactam_inhibitor',
       'cephems',
       'cephems',
       'cephems',
       'cephems',
       'tetracyclines',
       'b_lactam_inhibitor',
       'licosamide',
       'quinolones',
       'quinolones',
       'phenicols',
       'quinolones',
       'aminoglycosides',
       'tetracyclines',
       'lipopeptides',
       'aminoglycosides',
       'aminoglycosides',
       'b_lactam_inhibitor',
       'folate_path',
       'folate_path',
       'folate_path',
       'b_lactam_inhibitor',
       'pleuromutilin',
       'penicillins',
       'tetracyclines',
       'macrolides',
       'b_lactam_inhibitor',
       'folate_path',
       'macrolides']



df = pd.DataFrame({'drug' : missing, 'category' :cat})
category = category.append(df, ignore_index = True)
for i in order:
    category.loc[category['category'] == i,'order'] = order.index(i)


category.set_index('drug', inplace = True)


# map a color to each drug
import seaborn as sns
lut = dict(zip(category['order'].sort_values().unique(), sns.color_palette("hls", len(category['order'].unique()))))
category['drug_color'] = category['order'].map(lut)



# save to file
category.sort_values(by = 'order', inplace = True)

category.to_pickle('/home/hermuba/data0118/drug_category')
