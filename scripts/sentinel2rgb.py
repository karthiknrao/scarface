import glob
import numpy as np
from osgeo import gdal
import scipy.misc as sm
import os
import arrow

imagedir = '../sentinel/images/*/*/*/*/*/*/0'
imagedir = '../sentinel/images/43/P/GQ/*/*/*/0'
imagedir = '../sentinel/images/45/Q/VG/2017/4/18/0'
imagedir = '../sentinel/images/43/Q/BB/2018/2/*/0'

imagedir = '../sentinel/images/43/R/DP/2018/2/7/0'

b2_files = glob.glob( os.path.join( imagedir, '*B02.jp2' ) )
b3_files = glob.glob( os.path.join( imagedir, '*B03.jp2' ) )
b4_files = glob.glob( os.path.join( imagedir, '*B04.jp2' ) )

def norm(band):
    band_min, band_max = band.min(), band.max()
    return ((band - band_min)/(band_max - band_min))

for i in range(len(b3_files)):
    try:
        b2_link = gdal.Open(b2_files[i])
        b3_link = gdal.Open(b3_files[i])
        b4_link = gdal.Open(b4_files[i])
            
        b2 = norm(b2_link.ReadAsArray().astype(np.float))
        b3 = norm(b3_link.ReadAsArray().astype(np.float))
        b4 = norm(b4_link.ReadAsArray().astype(np.float))

        rgb = np.dstack((b4,b3,b2))

        del b2, b3, b4
        date = map(int,b2_files[i].split('/')[6:9])
        print(date)
        ts = arrow.get(date[0],date[1],date[2]).timestamp
        print(ts)
        outname = 'punjab/' + str(ts) + '.tif'
        sm.toimage(rgb,cmin=np.percentile(rgb,2),cmax=np.percentile(rgb,98)).save(outname)
        print( 'Done ', outname )
    except:
        print( 'Error ', b2_files[i] )

