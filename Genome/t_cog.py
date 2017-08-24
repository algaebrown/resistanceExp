# this is a parser for Dr.Wu's cog output
f = open("../../ecoli.cog")
lists = f.readlines()

import pandas as pd
df = pd.DataFrame()
# column_name
column_name = []
for i in lists:
    splitted = str.split(i, '/t')
    column_name.append(splitted[0])
    print(splitted)
#print(column_name)
    
    
