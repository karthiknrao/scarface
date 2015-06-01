require 'torch'
require 'image'
require 'nn'
require 'optim'
require 'xlua'
require 'cunn'

parameters,gradParameters = model:getParameters()

trainLogger = optim.Logger(paths.concat('results', 'train.log'))
testLogger = optim.Logger(paths.concat('results', 'test.log'))

confusion = optim.ConfusionMatrix(classes)
batchSize = 100
-- train method
optimState = {
      learningRate = 0.01,
      weightDecay = 0.1,
      momentum = 0.1,
      learningRateDecay = 1e-5
   }
optimMethod = optim.sgd

function train()
   epoch = epoch or 1
   print ( 'Current Epoch => ' .. epoch )
   model:training()
   shuffler = torch.randperm(trainsize)
   
   for t = 1,trainData:size(),batchSize do
      xlua.progress(t, trainData:size())
      local inputs = {}
      local targets = {}
      for i = t,math.min(t+batchSize-1,trainData:size()) do
         local input = trainData.data[shuffler[i]]
         local target = trainData.labels[shuffler[i]]
	 input = input:double()
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
	    local output = model:forward(inputs[i]:cuda())
	    local err = criterion:forward(output, targets[i])
	    f = f + err
	    
	    local df_do = criterion:backward(output, targets[i])
	    model:backward(inputs[i]:cuda(), df_do)
	    confusion:add(output, targets[i])
	 end
	 gradParameters:div(#inputs)
	 f = f/#inputs
	 return f, gradParameters
      end
      optimMethod(feval, parameters, optimState)
   end
   print 'Train Confusion'
   print(confusion)
   print 'Train Accuracy'
   print( confusion.totalValid * 100 )
   trainLogger:add{['% mean class accuracy (train set)'] = confusion.totalValid * 100}
   confusion:zero()
   epoch = epoch + 1
end

function test()
   model:evaluate()
   for t = 1,testData:size() do
      local input = testData.data[t]
      --input = input:double()
      input = input:cuda()
      local target = testData.labels[t]
      local pred = model:forward(input)
      confusion:add(pred, target)
   end
   print 'Test Confusion'
   print(confusion)
   print 'Test Accuracy'
   print( confusion.totalValid * 100 )
   testLogger:add{['% mean class accuracy (test set)'] = confusion.totalValid * 100}
end
