require 'torch'
require 'nn'
require 'nnx'
require 'optim'
require 'image'

torch.setnumthreads(2)

dofile 'data.lua'
dofile 'load_pretrained_model.lua'
