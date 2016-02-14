import numpy as np
import cPickle, gzip, os
import urllib, pdb
from utils import tile_raster_images
import Image

def sigmoid(x):
    return 1/(1 + np.exp(-x))

class RBM():
    def __init__(self,num_v,num_h,lr):
        self.W = np.random.randn(num_h,num_v)
        self.c = np.random.randn(num_v,1)
        self.b = np.random.randn(num_h,1)
        self.hn = num_h
        self.vn = num_v
        self.lr = lr

    def sample_h(self,v):
        rng = np.random.rand
        ho = sigmoid(np.dot(self.W,v) + self.b)
        rsmpl = rng(*ho.shape)
        return np.array(rsmpl < ho,dtype=int)

    def sample_v(self,h):
        rng = np.random.rand
        vo = sigmoid(np.dot(self.W.T,h) + self.c)
        rsmpl = rng(*vo.shape)
        return np.array(rsmpl < vo,dtype=int)

    def free_energy(self,v):
        wb = np.dot(self.W,v) + self.b
        vb = np.dot(self.c.T,v)
        ht = (np.log(1+np.exp(wb)))
        return (-ht.sum(axis=0) - vb).sum(axis=1)

    def train(self,k,testv0):
        testvk = testv0
        for i in range(k):
            testhk = self.sample_h(testvk)
            testvk = self.sample_v(testhk)
        prob_hv0 = sigmoid(np.dot(self.W,testv0)+self.b)
        prob_hvk = sigmoid(np.dot(self.W,testvk)+self.b)
        deltaw = (np.dot(prob_hv0,testv0.T) - \
                 np.dot(prob_hvk,testvk.T))/testv0.shape[1]
        deltab = (prob_hv0 - prob_hvk).mean(axis=1)
        deltac = (testv0 - testvk).mean(axis=1)

        self.W += self.lr*deltaw
        self.b += self.lr*deltab.reshape((self.hn,1))
        self.c += self.lr*deltac.reshape((self.vn,1))


def readdataset():
    f = gzip.open('mnist.pkl.gz','rb')
    train_set,valid_set,test_set = cPickle.load(f)
    f.close()
    return np.array(train_set[0] > 0,dtype=int)

if __name__ == '__main__':
    if not os.path.exists('mnist.pkl.gz'):
        urllib.urlretrieve('http://deeplearning.net/data/mnist/mnist.pkl.gz')
    train_set = readdataset().T
    rbm = RBM(784,500,0.09)
    batchsize = 50
    kcd = 1
    for j in range(20):
        print 'Epoch ', j
        #if j == 10:
        #    rbm.lr = 0.0001
        #    print 'Dropping Learning Rate'
        for i in range(0,train_set.shape[1],batchsize):
            v0 = train_set[:,i:i+batchsize]
            rbm.train(kcd,v0)
            print rbm.free_energy(v0)
        print 'Saving Image'
        image = Image.fromarray(
            tile_raster_images(
            X=rbm.W,
            img_shape=(28, 28),
            tile_shape=(10, 10),
            tile_spacing=(1, 1)
            )
        )
        image.save('1_filters_at_epoch_%i.png' % j)
