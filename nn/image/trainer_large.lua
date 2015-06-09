require 'torch'
require 'image'
require 'nn'
require 'optim'
require 'xlua'
require 'cunn'

models_path ='face_detection'

parameters,gradParameters = model:getParameters()

trainLogger = optim.Logger(paths.concat('results', 'train.log'))
testLogger = optim.Logger(paths.concat('results', 'test.log'))

confusion = optim.ConfusionMatrix(classes)
batchSize = 100
-- train method
optimState = {
      learningRate = 0.1,
      weightDecay = 0.001,
      momentum = 0.9,
      learningRateDecay = 1e-5
   }
optimMethod = optim.sgd

function train()
   epoch = epoch or 1
   print ( 'Current Epoch => ' .. epoch )
   model:training()

   shuffler = torch.randperm(trainsize)
   traindata = torch.Tensor(batchSize,chn,width,height)
   trainlabels = torch.Tensor(batchSize)

   for t = 1,trainsize,batchSize do
      xlua.progress(t, trainsize)
      local inputs = {}
      local targets = {}

      count = 1
      for i = t,math.min(t+batchSize-1,trainsize) do
	 data = trainlist[shuffler[i]]
	 img = image.load(data[2])
	 traindata[count] = img
	 trainlabels[count] = data[1]
	 count = count + 1
      end

      trainData = {
	 data = traindata,
	 labels = trainlabels,
	 size = function() return count - 1 end
      }
      trainData.data = trainData.data:float()
      normTrain = normalizebatch( trainData )

      for i = 1,normTrain:size()do
         local input = normTrain.data[i]
         local target = normTrain.labels[i]
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
   local modelname = epoch .. '.net'
   local filename = paths.concat(models_path, modelname)
   os.execute('mkdir -p ' .. sys.dirname(filename))
   print('==> saving model to '..filename)
   torch.save(filename, model)
   confusion:zero()
   epoch = epoch + 1
end

function test()
   model:evaluate()
   
   shuffler = torch.randperm(testsize)
   testdata = torch.Tensor(batchSize,chn,width,height)
   testlabels = torch.Tensor(batchSize)

   for t = 1,testsize,batchSize do
      xlua.progress(t, testsize)
      local inputs = {}
      local targets = {}

      count = 1
      for i = t,math.min(t+batchSize-1,testsize) do
	 data = testlist[shuffler[i]]
	 img = image.load(data[2])
	 testdata[count] = img
	 testlabels[count] = data[1]
	 count = count + 1
      end

      testData = {
	 data = testdata,
	 labels = testlabels,
	 size = function() return count - 1 end
      }
      testData.data = testData.data:float()
      normTest = normalizebatch( testData )

      for i = 1,normTest:size() do
         local input = normTest.data[i]
         local target = normTest.labels[i]
	 input = input:double()
         table.insert(inputs, input)
         table.insert(targets, target)
      end

   
      for t = 1,normTest:size() do
	 local input = normTest.data[t]
	 --input = input:double()
	 input = input:cuda()
	 local target = normTest.labels[t]
	 local pred = model:forward(input)
	 confusion:add(pred, target)
      end
   end
   print 'Test Confusion'
   print(confusion)
   print 'Test Accuracy'
   print( confusion.totalValid * 100 )
   testLogger:add{['% mean class accuracy (test set)'] = confusion.totalValid * 100}
end
