from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

cfg = { 
    'layers' : {
        'input' : {
            'type' : [ 'input', 1, 28 ]
            },
        'layer0' : {
            'input' : [ 'input' ],
            'type' : [ 'conv', 1, 32, 3 ]
            },
        'layer1' : {
            'input' : [ 'layer0', 'input' ],
            'type' : [ 'conv', 32, 64, 4 ]
            },
        'layer2' : {
            'input' : [ 'layer0', 'layer1' ],
            'type' : [ 'conv', 32, 64, 3 ]
            }
        'layer3' : {
            'input' : [ 'layer2' ],
            'type' : [ 'conv', 64, 128, 3 ]
            }
        }
}

def fix_network(cfg):
    nolayers = len(cfg['layers'].keys())
    for i in range(1,nolayers-1):
        key = 'layer' + str(i)
        inputs = cfg['layers'][key]['input']
        incoming = 0
        if cfg['layers'][key]['type'][0] == 'conv':
            for inp in inputs:
                incoming += cfg['layers'][inp]['type'][2]
            cfg['layers'][key]['type'][1] = incoming
        #elif cfg['layers'][key]['type'][0] == 'dense':
            
    return cfg

class MakeNet(nn.Module):
    def __init__(self,cfg):
        super(MakeNet,self).__init__()
        self.cfg = cfg
        self.layers = {}
        for layers in self.cfg['layers'].keys():
            if self.cfg['layers'][layers]['type'] == 'conv':
                incoming = self.cfg['layers'][layers]['type'][1]
                outcoming = self.cfg['layers'][layers]['type'][2]
                kernel = self.cfg['layers'][layers]['type'][3]
                self.layers[layers] = nn.Conv2d(incoming, outcoming, kernel_size=kernel)
            if self.cfg['layers'][layers]['type'] == 'dense':
                incoming = self.cfg['layers'][layers]['type'][1]
                outcoming = self.cfg['layers'][layers]['type'][2]
                self.layers[layers] = nn.Linear(incoming, outcoming)
                
    def forward(self,x):
        for i in range(1,nolayers-1):
            key = 'layer' + str(i)
            
        

if __name__ == '__main__':
    print( 'cfg before ' )
    print( cfg )
    cfg = fix_network(cfg)
    print( 'cfg after ' )
    print( cfg )
