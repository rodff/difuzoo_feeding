from astropy.io import fits
from astropy.nddata import Cutout2D
import astropy.nddata as apynd
import matplotlib.pyplot as plt
import numpy as np
import aplpy as apl
import sys

point = str(sys.argv[1])
bnd = str(sys.argv[2])
pct = float(sys.argv[3])     # Percentile

# INPUT
drt = 'point_{0}_{1}/'.format(point,bnd)
big_fn = '/home/rodrigoff96/siens/UDGs_Marco/point_{0}_{1}.fits'.format(point,bnd)
sz = 630
print('Percentile: '+str(pct))

# Load big image
hdul = fits.open(big_fn)

for k in range(1,len(hdul)):
    data = hdul[k].data
    Imax = np.percentile(data,pct)
    Ny = int(round(data.shape[0]/float(sz)))
    Nx = int(round(data.shape[1]/float(sz)))
    for i in range(0,Nx):
        for j in range(0,Ny):
            x = (0.5+i)*sz
            y = (0.5+j)*sz
            print(x,y)
            cut = Cutout2D(data, (x,y), sz, mode='partial')

            hdu_i = fits.ImageHDU(data=cut.data)

            out_fn = 'cut_{0}_{1}_{2}'.format(k,int(x),int(y))

            # Create scales and figures
            f = apl.FITSFigure(hdu_i)
            f.show_grayscale(stretch='asinh',vmax=Imax)

            f.ticks.hide()
            f.tick_labels.hide()
            f.axis_labels.hide()

            f.save(drt+out_fn+'_asinh_{0}.png'.format(pct),dpi=300)
            plt.close('all')