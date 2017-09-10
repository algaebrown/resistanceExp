# import
import pandas as pd

# read file
df = pd.read_pickle("../../data/clean_df")


# import package
from micToris import *

# main
for index,row in df.iterrows():
    # remove those without MIC value or have no standard
    if row['Measurement Value'] != 'nan':
        c_row = mic_to_ris(row)

        if type(c_row) != int:

            if type(c_row) != pd.core.series.Series:
                 c_row = c_row.iloc[0] # this converts c_row to series

            drug_inhibitor =row['Measurement Value'].split('/')
            r_break = c_row['R_breakpoint(>=)'].split('/')
            s_break = c_row['S_breakpoint(<=)'].split('/')

            # sometimes inhibitor criteria R and S is the same, then we only need to look at the drug
            if len(r_break) > 1:
                if r_break[1] == s_break[1]:
                    if len(drug_inhibitor) > 1:
                        drug_inhibitor = drug_inhibitor[:-1]

            result = []
            for i in range(len(drug_inhibitor)):
                # compare for both of them with standard
                interpret = compare_mic(
                    float(drug_inhibitor[i]),
                    row['Measurement Sign'],
                    float(r_break[i]),
                    float(s_break[i]))
                result.append(interpret)

                # make decision: choose the worst outcome
            ans = ['Resistant', 'Non-susceptible', 'Intermediate', 'Not defined', 'Susceptible']
            final_interpret = result[0] # default as one drug
            for a in ans:
                if a in result:
                    final_interpret = a


            # save
            df.ix[index, 'Resistant Phenotype']  = final_interpret
    else:
        print(row[['Antibiotic', 'Genome ID']], "no guide")


df.to_pickle("../../data/anno_df")
