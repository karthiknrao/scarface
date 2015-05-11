function splittsv(inputstr)
   local t={} ; i=1
   for str in string.gmatch(inputstr, "([^".."\t".."]+)") do
      t[i] = str
      i = i + 1
   end
   return t
end

filetr = "/home/indix/src/work/Crepe/data/train.tsv"
filete = "/home/indix/src/work/Crepe/data/test.tsv"
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"
datalen = 1014

print( 'Building Map ..' )
encodingmap = {}
for i = 1, string.len(alphabet) do
   local arr = torch.Tensor(69)
   arr:zero()
   arr[i] = 1
   encodingmap[string.sub(alphabet,i,i)] = arr
end

print( 'Reading Files ..' )
j = 1
strings = {}
label = {}
for line in io.lines(filetr) do
   values = splittsv(line)
   strings[j] = values[2]
   label[j] = values[1]
   j = j + 1
end
trainsize = j - 1
trainData = {
   data = strings,
   labels = label,
   size = function() return trainsize end
}
j = 1
strings2 = {}
label2 = {}
for line in io.lines(filete) do
   values = splittsv(line)
   strings2[j] = values[2]
   label2[j] = values[1]
   j = j + 1
end
testsize = j - 1
testData = {
   data = strings2,
   labels = label2,
   size = function() return testsize end 
}

--print( "TrainData" )
--print( trainData.data[10] )
--print( trainData.labels[10] )
classes = { "1","2","3","4","5","6","7","8","9","10","11","12","13","14" }
--classesmap = { ["1"] = 1, ["2"] = 2, ["3"] = 3, ["4"] = 4, ["5"] = 5, ["6"] = 6, ["7"] = 7, ["8"] = 8, ["9"] = 9, ["10"] = 10, ["11"] = 11, ["12"] = 12, ["13"] = 13, ["14"] = 14 }
function gettrainbatch(size,t)
   local inputs = {}
   local targets = {}
   for i = t, math.min(t+size-1,trainData:size()) do
      --print(i)
      --print(trainData.data[shuffler[i]])
      local input = trainData.data[shuffler[i]]
      local target = trainData.labels[shuffler[i]]
      table.insert(inputs, input)
      table.insert(targets, target)
   end
   local batchi = {}
   batchi['inputs'] = inputs
   batchi['targets'] = targets
   return batchi
end

function encodeinput(inp)
   local tinput = torch.Tensor(batchSize,datalen,string.len(alphabet))
   local ttarget = torch.Tensor(batchSize)
   local strings = inp["inputs"]
   local targets = inp["targets"]
   for i=1, #strings do
      str = strings[i]
      --print(targets[i])
      tinp = torch.Tensor(datalen,string.len(alphabet))
      if string.len(str) < 1014 then
	 str = str .. string.rep( ' ', 1014 - string.len(str) )
      end
      for j=1, string.len(str) do
	 if encodingmap[string.sub(str,j,j)] == nil then
	    tarr = torch.Tensor(69)
	    tarr:zero()
	    tinput[i][j] = tarr
	 else
	    tinput[i][j] = encodingmap[string.sub(str,j,j)]
	 end
      end
      ttarget[i] = tonumber(targets[i])
   end
   local encodedinp = {}
   encodedinp["inputs"] = tinput
   encodedinp["targets"] = ttarget
   return encodedinp
end
