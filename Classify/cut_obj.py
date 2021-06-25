from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
#import astropy.nddata as apynd
import matplotlib.pyplot as plt
import numpy as np
import aplpy as apl
import sys

point = str(sys.argv[1])        # Pointing
bnd = str(sys.argv[2])          # Band
ra = float(sys.argv[3])       # Right Ascension
dec = float(sys.argv[4])      # Declination
drt = str(sys.argv[5])      # Output directory 

# INPUT
big_fn = '/home/rodrigoff96/siens/UDGs_Marco/point_{0}_{1}.fits'.format(point,bnd)
sz = 400    # Size of the figure
stch = 'asinh'   # Strech of the scale

pos = SkyCoord(ra,dec, unit='deg', frame='fk5')
hdul = fits.open(big_fn)

# Search for object in mosaic
for i in range(1,len(hdul)):
    Twcs = WCS(hdul[i].header,hdul)
    if(Twcs.footprint_contains(pos)):
        Owcs = Twcs
        Tn = i
        data = hdul[Tn].data
        print('FOUND in extension {0}'.format(Tn))
        break
    else:
        #print('Not in extension {0}'.format(i))
        pass


try:
    # Convert ra,dec to pixels
    x,y = Owcs.all_world2pix(ra,dec,1)

    # Cutout
    cut = Cutout2D(data, (x,y), sz, mode='partial')

    hdu_i = fits.ImageHDU(data=cut.data)
    out_fn = 'obj_{0}_{1}_{2}_{3}'.format(point,Tn,int(x),int(y))

    # Create images using different percentiles for the maximum brightness
    for pct in [99.7,99.8]:

        drt_i = drt+'/'+str(pct)

        # Get maximum
        Imax = np.percentile(data,pct)

        # Create scales and figures
        f = apl.FITSFigure(hdu_i)
        f.show_grayscale(stretch=stch,vmax=Imax)

        f.ticks.hide()
        f.tick_labels.hide()
        f.axis_labels.hide()

        f.save('{0}/{1}_{2}_{3}.png'.format(drt_i,out_fn,stch,pct),dpi=350)
        plt.close('all')
except:
    print('Object not found in this pointing.')