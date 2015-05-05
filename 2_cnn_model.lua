require 'torch'
require 'image'
require 'nn'
require 'optim'

n_out = 10
chn = 1
width = 32
height = 32
batchSize = 100
train_file = 'train_32x32.t7'
test_file = 'test_32x32.t7'
trsize = 73257
tesize = 26032

print 'Loading Datasets ... '

loaded = torch.load(train_file,'ascii')
trainData = {
   data = loaded.data:transpose(3,4),
   labels = loaded.labels[1],
   size = function() return trsize end
}

loaded = torch.load(test_file,'ascii')
testData = {
   data = loaded.data:transpose(3,4),
   labels = loaded.labels[1],
   size = function() return tesize end
}

trainData.data = trainData.data:float()
testData.data = testData.data:float()

print 'Normalize Data ... '

for i = 1,trainData:size() do
   trainData.data[i] = image.rgb2yuv(trainData.data[i])
end
for i = 1,testData:size() do
   testData.data[i] = image.rgb2yuv(testData.data[i])
end

channels = {'y','u','v'}

print 'Normalize each channel globally'
mean = {}
std = {}
for i,channel in ipairs(channels) do
   -- normalize each channel globally:
   mean[i] = trainData.data[{ {},i,{},{} }]:mean()
   std[i] = trainData.data[{ {},i,{},{} }]:std()
   trainData.data[{ {},i,{},{} }]:add(-mean[i])
   trainData.data[{ {},i,{},{} }]:div(std[i])
end

print 'Normalize test data, using the training means/stds'
-- Normalize test data, using the training means/stds
for i,channel in ipairs(channels) do
   -- normalize each channel globally:
   testData.data[{ {},i,{},{} }]:add(-mean[i])
   testData.data[{ {},i,{},{} }]:div(std[i])
end

neighborhood = image.gaussian1D(13)
print 'Spatital ContrativeNorm'
normalization = nn.SpatialContrastiveNormalization(1, neighborhood, 1):float()
for c in ipairs(channels) do
   for i = 1,trainData:size() do
      if i % 500 == 0 then
	 print ( i )
      end
      trainData.data[{ i,{c},{},{} }] = normalization:forward(trainData.data[{ i,{c},{},{} }])
   end
   for i = 1,testData:size() do
      testData.data[{ i,{c},{},{} }] = normalization:forward(testData.data[{ i,{c},{},{} }])
   end
end

print 'Create Model ...'
-- start model
model = nn.Sequential()
-- layer1
model:add(nn.SpatialConvolution(chn, 64, 5, 5))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
-- layer2
model:add(nn.SpatialConvolution(64, 64, 3, 3))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
-- layer3
model:add(nn.Reshape(64*6*6))
model:add(nn.Linear(64*6*6, 100))
model:add(nn.ReLU())
model:add(nn.Linear(100,n_out))

model:add(nn.LogSoftMax())

criterion = nn.ClassNLLCriterion()

parameters,gradParameters = model:getParameters()

classes = {'1','2','3','4','5','6','7','8','9','0'}

trainLogger = optim.Logger(paths.concat('results', 'train.log'))
testLogger = optim.Logger(paths.concat('results', 'test.log'))

confusion = optim.ConfusionMatrix(classes)

-- train method
optimState = {
      learningRate = 0.001,
      weightDecay = 0,
      momentum = 0,
      learningRateDecay = 1e-7
   }
optimMethod = optim.sgd

--- training

function train()
   epoch = epoch or 1
   print ( 'Epoch Current => ' .. epoch )
   model:training()
   shuffle = torch.randperm(trsize)
   
   for t = 1,trainData:size(),batchSize do
      -- disp progress
      -- xlua.progress(t, trainData:size())

      -- create mini batch
      local inputs = {}
      local targets = {}
      for i = t,math.min(t+batchSize-1,trainData:size()) do
         -- load new sample
         local input = trainData.data[shuffle[i]]
         local target = trainData.labels[shuffle[i]]
	 input = input:double()
         --if opt.type == 'double' then input = input:double()
         --elseif opt.type == 'cuda' then input = input:cuda() end
         table.insert(inputs, input)
         table.insert(targets, target)
      end

      local feval = function(x)
	 if x ~= parameters then
	    parameters:copy(x)
	 end
	 gradParameters:zero()
	 local f = 0
	 for i = 1, #inputs do
	    local output = model:forward(inputs[i])
	    local err = criterion:forward(output, targets[i])
	    f = f + err
	    
	    local df_do = criterion:backward(output, targets[i])
	    model:backward(inputs[i], df_do)
	    confusion:add(output, targets[i])
	 end
	 gradParameters:div(#inputs)
	 f = f/#inputs
	 return f, gradParameters
      end
      optimMethod(feval, parameters, optimState)
   end
   --print( 'mean class accuracy (train set)' .. confusion.totalValid * 100 )
   trainLogger:add{['% mean class accuracy (train set)'] = confusion.totalValid * 100}
   print(confusion)
   confusion:zero()
   epoch = epoch + 1
end

function test()
   model:evaluate()
   for t = 1,testData:size() do
      
      local input = testData.data[t]
      input = input:double()
      local target = testData.labels[t]

      -- test sample
      local pred = model:forward(input)
      --print ( pred  )
      --print ( target )
      confusion:add(pred, target)
   end
   testLogger:add{['% mean class accuracy (test set)'] = confusion.totalValid * 100}
   print( 'mean class accuracy (test set)' .. confusion.totalValid * 100 )
   confusion:zero()
end

print 'Start Training ...'
for counter = 1, 100 do
   train()
   test()
end
