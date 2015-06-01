require 'nn'
require 'image'
require 'optim'
require 'torch'
require 'cunn'

model = nn.Sequential()

--layer1
model:add(nn.SpatialConvolution(3,128, 5, 5, 1, 1))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
--layer2
model:add(nn.SpatialConvolution(128,256, 5, 5, 1, 1))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
--layer3
model:add(nn.SpatialZeroPadding(1, 1, 1, 1))
model:add(nn.SpatialConvolution(256, 512, 4, 4, 1, 1))
model:add(nn.ReLU())
--layer4
model:add(nn.Reshape(4*4*512))
model:add(nn.Linear(4*4*512,1000))
model:add(nn.ReLU())
model:add(nn.Linear(1000,#classes))

model:add(nn.LogSoftMax())
criterion = nn.ClassNLLCriterion()

print(model)

model:cuda()
criterion:cuda()
