require 'torch'
require 'image'
require 'nn'
require 'optim'
require 'xlua'

parameters,gradParameters = model:getParameters()

trainLogger = optim.Logger(paths.concat('results', 'train.log'))
testLogger = optim.Logger(paths.concat('results', 'test.log'))

confusion = optim.ConfusionMatrix(classes)
batchSize = 128
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
   print("trainsize")
   print(trainsize)
   shuffler = torch.randperm(trainsize)
   
   for t = 1,trainData:size(),batchSize do
      xlua.progress(t, trainData:size())
      currbatch = gettrainbatch(batchSize,t)
      einputs = encodeinput(currbatch)
      inputs = einputs["inputs"]
      targets = einputs["targets"]
      --print(targets)
      local feval = function(x)
	 if x ~= parameters then
	    parameters:copy(x)
	 end
	 gradParameters:zero()
	 local f = 0
	 for i = 1, inputs:size()[1] do
	    local output = model:forward(inputs[i])
	    --print("outputSize")
	    --print(output:size())
	    local err = criterion:forward(output, targets[i])
	    f = f + err
	    local df_do = criterion:backward(output, targets[i])
	    model:backward(inputs[i], df_do)
	    confusion:add(output, targets[i])
	 end
	 gradParameters:div(inputs:size()[1])
	 f = f/inputs:size()[1]
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
      input = input:double()
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
