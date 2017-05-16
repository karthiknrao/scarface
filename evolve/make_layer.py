import theano
import theano.tensor as T
from lasagne.layers import Conv2DLayer, InputLayer
from lasagne.layers import ElemwiseSumLayer
import lasagne
import random
import numpy as np

num_nodes = 5
list_len = int((num_nodes - 1)*(num_nodes - 2)/2)
binary_list = [ [ 1 if random.random() < 0.5 else 0 for i in range(node) ] for node in range(1,num_nodes) ]

def get_output_nodes(blist):
    node_outs = []
    for i in range(len(blist)):
        out = 0
        for node in blist[i:]:
            out += node[i]
        node_outs.append(out)
    return ( [ k for k, val in enumerate(node_outs) if val > 0 ], \
                 [ k for k, val in enumerate(node_outs) if val == 0 ] + [ num_nodes - 1 ] )

def get_isolated_nodes(no_out,no_in):
    outset = set(no_out)
    inset = set(no_in)
    return list(outset.intersection(inset))

def create_stage(incoming,binary_list):
    layers = []
    testx = T.tensor4()
    if isinstance(incoming,type(testx)):
        x = InputLayer(shape=(None,1,20,20),input_var=X)
        layers.append( Conv2DLayer(x,num_filters=32,filter_size=(3,3),pad='same') )
    else:
        x = incoming
        layers.append( Conv2DLayer(incoming,num_filters=32,filter_size=(3,3),pad='same') )

    for i, layer in enumerate(binary_list):
        if i == 0:
            if layer[0] == 0:
                layers.append( Conv2DLayer(x,num_filters=32,filter_size=(3,3), pad='same') )
            else:
                layers.append( Conv2DLayer(layers[0],num_filters=32,filter_size=(3,3), pad='same') )
        else:
            if sum(layer) == 0:
                layers.append( Conv2DLayer(x,num_filters=32,filter_size=(3,3),pad='same') )
            else:
                in_edges = []
                for k, edge in enumerate(layer):
                    if edge == 1:
                        in_edges.append(layers[k])
                o = ElemwiseSumLayer(in_edges)
                layers.append( Conv2DLayer(o,num_filters=32,filter_size=(3,3), pad='same') )
    
    output_nodes, no_outputs = get_output_nodes(binary_list)
    no_inputs = [ k for k, node in enumerate(binary_list) if sum(node) == 0 ]
    isolated_nodes = get_isolated_nodes(no_outputs,no_inputs)
    outputs = [ layers[i] for i in output_nodes ]
    o = ElemwiseSumLayer(outputs)
    o = Conv2DLayer(o,num_filters=32,filter_size=(3,3), pad='same' )
    print( 'List :', binary_list )
    print( 'Output nodes :', output_nodes )
    print( 'Isolated_nodes :', isolated_nodes )
    print( 'No Output nodes :', no_outputs )
    print( 'No Input nodes :', no_inputs )

    return o

stages = [ 4, 5 ]
outs = []
for i, num_nodes in enumerate(stages):
    binary_list = [ [ 1 if random.random() < 0.5 else 0 for i in range(node) ] for node in range(1,num_nodes) ]
    if i == 0:
        X = T.tensor4()
        o = create_stage(X,binary_list)
        outs.append(o)
    else:
        o_inter = lasagne.layers.MaxPool2DLayer(outs[-1],pool_size=(2,2))
        o = create_stage(o_inter,binary_list)
        outs.append(o)

net_out = lasagne.layers.get_output(outs[-1])
func = theano.function( [X], net_out )
xx = np.random.randn(2,1,20,20)
yy = func(xx)
print(yy.shape,xx.shape)
