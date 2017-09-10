import pandas as pd
# for each row
clsi = pd.read_excel("../../data/CLSI_m100_breakpoint.xlsx", converters = {'R_breakpoint(>=)': str, 'S_breakpoint(<=)': str})

def identify_sps(row):

    if 'Pseudomonas' in row['Genome Name']:
        sps = 'Pseudomonas aeruginosa'
    elif 'Acinetobacter' in row['Genome Name']:
        sps = 'Acinetobacter spp.'
    else:
        sps = 'Enterobacteriae'
    return(sps)

def mic_to_ris(row):
    sps = identify_sps(row)
    possible = clsi.loc[(clsi['family'] == sps) & (clsi['drug'] == row['Antibiotic'])]
    right = 0 # initiate as 0

    # if only one criteria found, use that one
    if list(possible.shape)[0] == 1:
        right = possible

    # if more than one was found, then choose the right one
    else:

        # check possible criteria one by one
        for index, c_row in possible.iterrows():
            # if in include sps, use that criteria and leave the cheking loop
            if c_row.notnull()['species']:
                include_sps = c_row['species'].split(', ')
                for i in include_sps:
                    name_split = i.split(' ')
                    if name_split[0] in row["Genome Name"] :
                        right = c_row
                        break
            if type(right) == pd.core.series.Series:
                break
            elif c_row.isnull()['species'] and c_row.notnull()['not_species']:
                exclude = 0
                exclude_sps = c_row['not_species'].split(', ')
                for i in exclude_sps:
                    name_list = row['Genome Name'].split(' ')
                    if name_list[0] in i:

                        exclude = 1
                if exclude == 0:
                    right = c_row

            if type(right) == pd.core.series.Series:
                break
            elif c_row.isnull()['not_species'] and c_row.isnull()['species']:
                right = c_row


    return(right) # right will be the row containing criteria. if right is 0, that means no criteria fits.



def compare_mic(measurement, sign, r_break, s_break):
    if measurement >= r_break:
        if sign in ['<', '<=']:
            result = "Not defined"
        else:
            result = "Resistant"
    elif measurement <= s_break:
        if sign in ['>', '>=']:
            result = "Non-susceptible"
        else:
            result = "Susceptible"
    else:
        if type(sign) == float:
            result = "Intermediate"
        elif sign in ['>=', ">"]:
            result = "Non-susceptible"
        else:
            result = "Not defined"

    return(result)
