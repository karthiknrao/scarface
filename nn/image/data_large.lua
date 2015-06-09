require 'lfs'
require 'image'
require 'math'
require 'nn'

dataset = '/data/misc/lfw_r/'
classes = {}
chn = 3
width = 227
height = 227

for file in lfs.dir(dataset) do
   if file ~= '.' and file ~= '..' then
      table.insert( classes, file )
   end
end

datafiles = {}
for i,dirs in pairs(classes) do
   for file in lfs.dir(dataset .. dirs) do
      if file ~= '.' and file ~= '..' then
	 label = dirs
	 filepath = dataset .. dirs .. "/" .. file
	 --print(filepath)
	 table.insert(datafiles, { label, filepath } )
      end
   end
end

print 'Number of files'
print( #datafiles )

shuffle = torch.randperm(#datafiles)
testsize = math.floor(#datafiles*0.1)
trainsize = #datafiles - testsize

trainlist = {}
testlist = {}

for i = 1, trainsize do
   table.insert(trainlist, datafiles[shuffle[i]])
end

for i = trainsize + 1, #datafiles do
   table.insert(testlist, datafiles[shuffle[i]])
end

function normalizebatch( imgs )
  for i = 1,imgs:size() do
     imgs.data[i] = image.rgb2yuv(imgs.data[i])
   end

   channels = {'y','u','v'}
   mean = {}
   std = {}
   for i,channel in ipairs(channels) do
   -- normalize each channel globally:
      mean[i] = imgs.data[{ {},i,{},{} }]:mean()
      std[i] = imgs.data[{ {},i,{},{} }]:std()
      imgs.data[{ {},i,{},{} }]:add(-mean[i])
      imgs.data[{ {},i,{},{} }]:div(std[i])
   end
   
   neighborhood = image.gaussian1D(13)
   normalization = nn.SpatialContrastiveNormalization(1, neighborhood, 1):float()

   for c in ipairs(channels) do
      for i = 1,imgs:size() do
	imgs.data[{ i,{c},{},{} }] = normalization:forward(imgs.data[{ i,{c},{},{} }])
      end
   end
   return imgs
end
