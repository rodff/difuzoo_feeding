from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
#import numpy as np
import sys

point = str(sys.argv[1])
bnd = str(sys.argv[2])
ra = float(sys.argv[3])       # Right Ascension
dec = float(sys.argv[4])      # Declination

big_fn = '/home/rodrigoff96/siens/UDGs_Marco/point_{0}_{1}.fits'.format(point,bnd)

pos = SkyCoord(ra,dec, unit='deg', frame='fk5')

# Load big image
hdul = fits.open(big_fn)

for i in range(1,len(hdul)):
    Twcs = WCS(hdul[i].header,hdul)
    if(Twcs.footprint_contains(pos)):
        Owcs = Twcs
        Tn = i
        print('FOUND in extension (tile) {0}'.format(Tn))
        break
    else:
        print('Not in extension (tile) {0}'.format(i))

try: 
    x,y = Owcs.all_world2pix(ra,dec,1)
    dt = hdul[Tn].data
    dims = (dt.shape[1],dt.shape[0])    # Just because numpy arrays give y,x instead of x,y pixel coordinates
    print('\n File: {0} \n Extension: {1} \n Dimensions: {2} \n X: {3} \n Y: {4} \n'.format(big_fn,Tn,dims,x,y))
except:
    print('Object with coord. ({0},{1}) not found in the given WCS object.'.format(ra,dec))