import theano
import theano.tensor as T
import lasagne

X = T.tensor4()
x = lasagne.layers.InputLayer(shape=(None,1,20,20),input_var=X)
c = lasagne.layers.Conv2DLayer(x,num_filters=10,filter_size=(3,3))

print( 'tensor :', type(X) )
print( 'conv :', type(c) )
