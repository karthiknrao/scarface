require 'nn'
require 'image'
require 'optim'
require 'torch'
require 'cunn'

model = nn.Sequential()
--layer1
model:add(nn.SpatialZeroPadding(2,2,2,2))
model:add(nn.SpatialConvolution(3,96,11,11,4,4))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(3,3,2,2))
--layer2
model:add(nn.SpatialZeroPadding(2,2,2,2))
model:add(nn.SpatialConvolution(96,256,5,5,1,1))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(3,3,2,2))
--layer3
model:add(nn.SpatialZeroPadding(1,1,1,1))
model:add(nn.SpatialConvolution(256,384,3,3,1,1))
model:add(nn.ReLU())
--layer4
model:add(nn.SpatialZeroPadding(1,1,1,1))
model:add(nn.SpatialConvolution(384,384,3,3,1,1))
model:add(nn.ReLU())
--layer5
model:add(nn.SpatialZeroPadding(1,1,1,1))
model:add(nn.SpatialConvolution(384,256,3,3,1,1))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(3,3,2,2))
--layer6
model:add(nn.Reshape(6*6*256))
model:add(nn.Linear(6*6*256,4096))
model:add(nn.ReLU())
--layer7
model:add(nn.Linear(4096,4096))
model:add(nn.ReLU())
model:add(nn.Linear(4096,#classes))

model:add(nn.LogSoftMax())
criterion = nn.ClassNLLCriterion()
print(model)

model:cuda()
criterion:cuda()
