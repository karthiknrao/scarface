require 'nn'
require 'image'
require 'optim'
require 'torch'

model = nn.Sequential()
-- layer1
model:add(nn.SpatialConvolution(chn,4, 5, 5))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
-- layer2
model:add(nn.SpatialConvolution(4, 8, 5, 5))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
-- layer3
model:add(nn.Reshape(8*5*5))
model:add(nn.Linear(8*5*5, 100))
model:add(nn.ReLU())
model:add(nn.Linear(100,#classes))

model:add(nn.LogSoftMax())

criterion = nn.ClassNLLCriterion()

print(model)
