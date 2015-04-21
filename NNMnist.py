from ffnet import ffnet, mlgraph, readdata
import numpy as np
import sys

def readfile( fname ):
    lines = open( fname ).readlines()[1:]
    vec = [ map( float, x.split(',')[0:-1] ) for x in lines ]
    clas = [ x.split(',')[-1] for x in lines ]
    output = [ [1,0,0,0,0,0,0,0,0],
               [0,1,0,0,0,0,0,0,0],
               [0,0,1,0,0,0,0,0,0],
               [0,0,0,1,0,0,0,0,0],
               [0,0,0,0,1,0,0,0,0],
               [0,0,0,0,0,1,0,0,0],
               [0,0,0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0,1,0],
               [0,0,0,0,0,0,0,0,1] ]
    return vec, [ output[int(x.split('_')[-1])-1] for x in\
                       clas ]

if __name__ == '__main__':
    conec = mlgraph((94,30,30,9))
    net = ffnet(conec)
    tra, out = readfile( sys.argv[1] )
    tra = np.array(tra)
    out = np.array(out)
    net.train_tnc( tra, out, maxfun=2000, messages=1 )
