require 'torch'
require 'nn'
require 'nnx'
require 'optim'
require 'image'
require 'cunn'

model = torch.load( 'trained_models/10.net' )
print( 'Loading Trained Model..' )
print(model)

file = torch.DiskFile('1000_layer.val', 'w')
lfile = torch.DiskFile('1000_layer_l.val','w')
for t = 1, trainData:size() do
   local input = trainData.data[t]:cuda()
   local label = trainData.labels[t]
   local output = model:forward(input)
   layerOutput = model:get(12).output:float()
   file:writeFloat(layerOutput:storage())
   lfile:writeInt(label)
end
file:close()
lfile:close()

--print(model:forward(sample))
--print(model:get(12).output)
