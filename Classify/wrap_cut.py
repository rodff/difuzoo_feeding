import os
import sys
import pandas as pd 

fn = str(sys.argv[1])
point = str(sys.argv[2])
bnd = str(sys.argv[3])
drt = str(sys.argv[4])

df = pd.read_csv(fn)

idx = list(range(0,len(df)))

for i in idx:

    o = df.iloc[i]

    os.system('python cut_obj.py {0} {1} {2} {3} {4}'.format(point,bnd,o.ra,o.dec,drt))
    