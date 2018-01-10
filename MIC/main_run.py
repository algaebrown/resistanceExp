# import
import pandas as pd

# read file
df = pd.read_pickle("/home/hermuba/data0118/clean_data")


# import package
from micToris import *

def backup_old_anno(df):
    df['original_Phenotype'] = df['Resistant Phenotype']

# identify those who has MIC:
def with_mic(df):
    mic_index = df.loc[df['Measurement Value'].notnull()].index
    df.loc[mic_index, 'Testing Standard'] = 'CLSI'
    df.loc[mic_index, 'Testing Standard Year'] = '2017'
    return(mic_index)

# identify comnbinations
def with_combination(mic):
    combine = mic.loc[ mic['Antibiotic'].str.contains('-')]

    single = mic.drop(index = combine.index, inplace = False)

    return(combine.index, single.index)


def deal_combine(combine_index):
    for index in combine_index:
        row = df.loc[index, :]
        print(index)
        c_row = mic_to_ris(row)  # return the correct clsi rule
        if type(c_row) == int:
            df.loc[index, 'Testing Standard Year'] = 'No Criteria'
        else:
            if type(c_row) != pd.core.series.Series:
                c_row = c_row.iloc[0] # this converts c_row to series

            drug_inhibitor =row['Measurement Value'].split('/')
            sign = row['Measurement Sign']
            r_break = c_row['R_breakpoint(>=)'].split('/')
            s_break = c_row['S_breakpoint(<=)'].split('/')

            if r_break[1] == s_break[1] or len(drug_inhibitor) == 1:
                result = compare_mic(drug_inhibitor[0], sign,  r_break[0], s_break[0])
            else:
                result1 = compare_mic(drug_inhibitor[0], sign,  r_break[0], s_break[0])
                result2 = compare_mic(drug_inhibitor[1], sign,  r_break[1], s_break[1])
                if result1 == result2:
                    result = result1
                else:
                    order = ['Resistant', 'Non-susceptible', 'Intermediate', 'Non-resistant', 'Susceptible']
                    for i in order:
                        if i in [result1, result2]:
                            result = i
                            break
            df.loc[index, 'Resistant Phenotype'] = result

def deal_single(single_index):
    for index in single_index:
        row = df.loc[index, :]

        c_row = mic_to_ris(row)  # return the correct clsi rule
        if type(c_row) == int:
            df.loc[index, 'Testing Standard Year'] = 'No Criteria'
        else:
            if type(c_row) != pd.core.series.Series:
                c_row = c_row.iloc[0] # this converts c_row to series
            result = compare_mic(row['Measurement Value'], row['Measurement Sign'],  c_row['R_breakpoint(>=)'], c_row['S_breakpoint(<=)'])
            if result != df.loc[index, 'Resistant Phenotype']:
                print(result, row['Measurement Sign'], row['Measurement Value'],c_row['R_breakpoint(>=)'], c_row['S_breakpoint(<=)'])
            df.loc[index, 'Resistant Phenotype'] = result

def run_all(df):
    backup_old_anno(df)
    mic_index = with_mic(df)
    mic = df.loc[mic_index]
    combine_index, single_index = with_combination(mic)
    deal_combine(combine_index)
    deal_single(single_index)

run_all(df)

df.to_pickle("/home/hermuba/data0118/annotated_RIS/anno_df")
new = df.loc[df['Testing Standard Year'] == '2017']
discrepency = new.loc[new['original_Phenotype']!=new['Resistant Phenotype']]
discrepency.to_pickle("/home/hermuba/data0118/annotated_RIS/discrepency_df")
