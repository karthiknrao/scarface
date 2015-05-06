require 'lfs'
require 'image'
require 'math'
require 'nn'

dataset = ''
classes = {}
chn = 3
width = 32
height = 32

for file in lfs.dir(dataset) do
   table.insert( classes, file )
end

for i,file in pairs(classes) do
   if file == '.' or file == '..' then
      table.remove(classes,i)
   end
end

datafiles = {}
for i,dirs in pairs(classes) do
   for file in lfs.dir(dataset .. dirs) do
      if file ~= '.' and file ~= '..' then
	 label = dirs
	 filepath = dataset .. dirs .. "/" .. file
	 table.insert(datafiles, { label, filepath } )
      end
   end
end

print 'Number of files'
print( #datafiles )

shuffle = torch.randperm(#datafiles)
testsize = math.floor(#datafiles*0.1)
trainsize = #datafiles - testsize

print( 'TrainSize ..' .. trainsize )
print( 'TestSize ..' .. testsize )

testdata = torch.Tensor(testsize,chn,width,height)
testlabels = torch.Tensor(testsize)
traindata = torch.Tensor(trainsize,chn,width,height)
trainlabels = torch.Tensor(trainsize)

for i = 1, testsize do
   data = datafiles[shuffle[i]]
   img = image.load(data[2])
   testlabels[i] = data[1]
   testdata[i] = img
end

for i = testsize + 1, #datafiles do
   data = datafiles[shuffle[i]]
   img = image.load(data[2])
   trainlabels[i-testsize] = data[1]
   traindata[i-testsize] = img
end

trainData = {
   data = traindata,
   labels = trainlabels,
   size = function() return trainsize end
}

testData = {
   data = testdata,
   labels = testlabels,
   size = function() return testsize end
}

trainData.data = trainData.data:float()
testData.data = testData.data:float()

for i = 1,trainData:size() do
   trainData.data[i] = image.rgb2yuv(trainData.data[i])
end
for i = 1,testData:size() do
   testData.data[i] = image.rgb2yuv(testData.data[i])
end

channels = {'y','u','v'}

mean = {}
std = {}
for i,channel in ipairs(channels) do
   -- normalize each channel globally:
   mean[i] = trainData.data[{ {},i,{},{} }]:mean()
   std[i] = trainData.data[{ {},i,{},{} }]:std()
   trainData.data[{ {},i,{},{} }]:add(-mean[i])
   trainData.data[{ {},i,{},{} }]:div(std[i])
end

for i,channel in ipairs(channels) do
   -- normalize each channel globally:
   testData.data[{ {},i,{},{} }]:add(-mean[i])
   testData.data[{ {},i,{},{} }]:div(std[i])
end

neighborhood = image.gaussian1D(13)
normalization = nn.SpatialContrastiveNormalization(1, neighborhood, 1):float()

for c in ipairs(channels) do
   for i = 1,trainData:size() do
      trainData.data[{ i,{c},{},{} }] = normalization:forward(trainData.data[{ i,{c},{},{} }])
   end
   for i = 1,testData:size() do
      testData.data[{ i,{c},{},{} }] = normalization:forward(testData.data[{ i,{c},{},{} }])
   end
end
