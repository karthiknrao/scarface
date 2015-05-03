require 'torch'
require 'image'
require 'nn'
require 'optim'

n_out = 10
chn = 3
width = 32
height = 32
batchSize = 100

loaded = torch.load(train_file,'ascii')
trainData = {
   data = loaded.X:transpose(3,4),
   labels = loaded.y[1],
   size = function() return trsize end
}



-- start model
model = nn.Sequential()
-- layer1
model:add(nn.SpatialConvolution(chn, 2*chn, 5, 5))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2,2,2,2))
-- layer2
model:add(nn.SpatialConvolution(2*chn, 2*chn, 3, 3))
model:add(nn.ReLU())
model::add(nn.SpatialMaxPooling(2,2,2,2))
--layer3
model:add(nn.Reshape(2*chn*3*3))
model:add(nn.Linear(2*chn*3*3, 100))
model:add(nn.ReLU())
model:add(nn.Linear(100,n_out))

model:add(nn.LogSoftMax())

criterion = nn.ClassNLLCriterion()

parameters,gradParameters = model:getParameters()

classes = {}

confusion = optim.ConfusionMatrix(classes)

--- training

function train()
   epoch = epoch or 1
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
   epoch = epoch + 1
end

while true do
   train()
end
