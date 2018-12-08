'''
Created: 2018-12-02
Last modified: 2018-12-02
Purpose: To generate file format compatible with pan-genome analyzing tool, PanGP
Input: Pangenome matrix at `~/data0118/cdhit/clstr/pangenome_df/`
Output: file without comma, header, index(Cluster X)
'''

# input path
path = '/home/hermuba/data0118/cdhit/clstr/pangenome_df/'

# function
def to_panGP(fname):

    full_input = path + fname
    full_output = path + fname + '_pangp'

    lines = 0
    with open(full_input) as i:
        with open(full_output, 'a') as o:
            for l in i:
                if lines == 0:
                    pass
                else:

                    o.write(''.join(l.split(',')[1:]))
                lines += 1
