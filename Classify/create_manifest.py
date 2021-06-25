import pandas as pd 
import os
import sys

Odrt = str(sys.argv[1])

img1_L = []
img2_L = []

# Load list of files in one directory
figs = [f.name for f in os.scandir('{0}/99.7/'.format(Odrt)) if f.is_file()] 

maxsz = 1000000  

# Loop over files 
for fn1 in figs:

    sz = os.path.getsize('{0}/99.7/{1}'.format(Odrt,fn1))
    fn2 = fn1[:-8]+'99.8.png'

    if(sz<=maxsz):

        os.system('mv {1}/99.7/{0} {1}/{0} && mv {1}/99.8/{2} {1}/{2}'.format(fn1,Odrt,fn2))

        # Append img filenames to lists
        img1_L.append(fn1)
        img2_L.append(fn2)
    else:
        os.system('mv {1}/99.7/{0} {1}/big/{0} && mv {1}/99.8/{2} {1}/big/{2}'.format(fn1,Odrt,fn2))


# Create dataframe
df = pd.DataFrame({'image1':img1_L,'image2':img2_L})

# Save CSV
df.to_csv('{0}/manifest.csv'.format(Odrt),index=False)