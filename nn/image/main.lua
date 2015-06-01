require 'torch'
require 'nn'
require 'nnx'
require 'optim'
require 'image'

torch.setnumthreads(2)

dofile 'data.lua'
dofile 'model.lua'
dofile 'trainer.lua'

print 'Start Training..'

for counter = 1, 100 do
   train()
   test()
end
