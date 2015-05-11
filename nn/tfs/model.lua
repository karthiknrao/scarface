require 'nn'
require 'torch'

model = nn.Sequential()

model:add(nn.TemporalConvolution(69,256,7))
model:add(nn.ReLU())
model:add(nn.TemporalMaxPooling(3, 3))

model:add(nn.TemporalConvolution(256,256,7))
model:add(nn.ReLU())
model:add(nn.TemporalMaxPooling(3, 3))

model:add(nn.TemporalConvolution(256,256,3))
model:add(nn.ReLU())

model:add(nn.TemporalConvolution(256,256,3))
model:add(nn.ReLU())

model:add(nn.TemporalConvolution(256,256,3))
model:add(nn.ReLU())
model:add(nn.TemporalMaxPooling(3, 3))

model:add(nn.Reshape(8704))
model:add(nn.Linear(8704,1024))
model:add(nn.ReLU())
model:add(nn.Dropout(0.5))

model:add(nn.Linear(1024,1024))
model:add(nn.ReLU())
model:add(nn.Dropout(0.5))

model:add(nn.Linear(1024,14))
model:add(nn.LogSoftMax())

criterion = nn.ClassNLLCriterion()

print(model)
