import scipy.io.wavfile as sp
import glob
import os
import numpy as np
import numpy.random as npr

wavdir = 'wav'

dirs = os.listdir(wavdir)
fdata = []
outdir = 'data'

if not os.path.exists(outdir):
    os.mkdir(outdir)

for dname in dirs:
    dpath = os.path.join(wavdir,dname)
    files = glob.glob(os.path.join(dpath,'*'))
    for fname in files:
        data = sp.read(fname)
        fdata.append( (fname,data[0],int(len(data[1])/float(data[0]))) )

count = 0
for fname,sample,length in fdata:
    label = fname.split('/')[1]
    outpath = os.path.join(outdir,label)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    if sample == 8000:
        print fname
        (l,data) = sp.read(fname)
        for i in range(length-10):
            if label == 'happy':
                datas = data[i*8000:i*8000+8000*10]
                sname = os.path.join(outpath,str(count))
                np.save(sname,datas)
                count += 1
                for x in range(5):
                    datas = data[i*8000:i*8000+8000*10] + npr.normal(0,5,8000*10)
                    sname = os.path.join(outpath,str(count))
                    np.save(sname,datas)
                    count += 1

            else:
                datas = data[i*8000:i*8000+8000*10]
                sname = os.path.join(outpath,str(count))
                np.save(sname,datas)
                count += 1
                
