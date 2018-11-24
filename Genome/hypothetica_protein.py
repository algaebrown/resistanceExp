def hypothetical(df):
    hypo = df.loc[df['stitle'].str.contains('hypothetical') | df['stitle'].str.contains('ncharacter') | df['stitle'].str.contains('unknown')]

    df.loc[hypo.index, 'hypothetical'] = True

    return(df)
