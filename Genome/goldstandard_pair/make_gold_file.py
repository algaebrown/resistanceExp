import pandas as pd

def link_or_not(go_set1, go_set2, large_term_to_remove = None):
    ''' decide if there is term overlapping'''

    inter = go_set1.intersection(go_set2)
    if len(large_term_to_remove) > 0:
        [inter.remove(term) for term in large_term_to_remove if term in inter]

    if len(inter) > 0:
        answer = 1
    else:
        answer = 0


    return(answer)
    #out_df = out_df.append([[name1, name2, answer]])
    #print(out_df.shape)


    

def gold_standard(anno_df, term, outfile, large_term_to_remove = None):
    ''' generated goldstandard pair to validate network 
    anno_df: dataframe with annotation 'GO', 'pathway'
    
    '''
    # write header
    outfile = outfile + term
    with open(outfile, 'w') as f:
        f.write('gene_one,gene_two,goldstandard\n')

    s = anno_df[term].dropna() # remove nan
    import itertools

    all_pairs = itertools.combinations(s.index, 2)


    itxn = []
    n1 = []
    n2 = []
    for p in all_pairs:
        l = link_or_not(s[p[0]], s[p[1]], large_term_to_remove)
        itxn.append(l)
        n1.append(p[0])
        n2.append(p[1])

        with open(outfile, 'a') as f:
            f.write(','.join([p[0], p[1], str(l)])+'\n')
    #return(n1, n2, itxn)
