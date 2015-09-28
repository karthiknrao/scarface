import os
import sys
import glob

dirs = [ 'angry','happy','unhappy','neutral' ]
outpath = 'wav'
if not os.path.exists(outpath):
    os.mkdir(outpath)
for dname in dirs:
    files = glob.glob(os.path.join( dname, '*' ))
    outdir = os.path.join(outpath,dname)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for fname in files:
        filename = os.path.basename(fname)
        outfname = os.path.join(outdir,filename).split('.')[0] + '.wav'
        cmd = 'sox "%s" "%s"' % ( fname, outfname )
        os.system(cmd)
