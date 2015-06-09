require 'torch'
require 'nn'
require 'nnx'
require 'optim'
require 'image'

torch.setnumthreads(2)

dofile 'data_large.lua'
dofile 'models/alexnet.lua'
dofile 'trainer_large.lua'

print 'Start Training..'

for counter = 1, 100 do
   train()
   test()
end
