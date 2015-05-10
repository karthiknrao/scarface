function splittsv(inputstr)
   local t={} ; i=1
   for str in string.gmatch(inputstr, "([^".."\t".."]+)") do
      t[i] = str
      i = i + 1
   end
   return t
end

filen = "/home/karthik/src/Crepe/data/dbpedia_csv/train.csv"
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"

print( 'Building Map ..' )
encodingmap = {}
for i = 1, string.len(alphabet) do
   local arr = torch.Tensor(69)
   arr:zero()
   arr[i] = 1
   encodingmap[string.sub(alphabet,i,i)] = arr
end

print( 'Reading File ..' )
stringlinemap = {}
j = 1
for line in io.lines(filen) do
   values = splittsv(line)
   stringlinemap[j] = values
   j = j + 1
end

function gettrainbatch()
   
end

print(stringlinemap[10])
