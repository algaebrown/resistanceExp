def identify_hypothetical(df):

    '''
    a script to take parsed diamond/blast nr dataframe, identify hypothetical proteins
    input: dataframe generated from Genome.annotate_parser.parse_blast.parse_diamond()
    output: dataframe with additional column "hypothetical"; True includes either "hypothetical protein, unknown protein, and uncharacterized protein"
    '''
    hypo = df.loc[df['stitle'].str.contains('hypothetical') | df['stitle'].str.contains('ncharacter') | df['stitle'].str.contains('unknown') | df['stitle'].str.contains('DUF')]

    df.loc[hypo.index, 'hypothetical'] = True

    return(df)
