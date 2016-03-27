from PIL import Image
import os

class ImageSequence:
    def __init__(self, im):
        self.im = im
    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
            raise IndexError

files = [ 'test-volume.tif','train-labels.tif','train-volume.tif' ]

if not os.path.exists('train'):
    os.mkdir('train')
if not os.path.exists('labels'):
    os.mkdir('labels')

train = Image.open( files[1] )
for i in range(30):
    train.save( os.path.join( 'labels', 'frame%d.tif' % i ) )
    if i+1 > 29:
        break
    train.seek(i+1)


test = Image.open( files[2] )
for i in range(30):
    test.save( os.path.join( 'train', 'frame%d.tif' % i ) )
    if i+1 > 29:
        break
    test.seek(i+1)
    
