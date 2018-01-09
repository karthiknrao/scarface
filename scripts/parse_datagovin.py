import xmltodict
import sys
import pdb

fname = sys.argv[1]

with open(fname) as fd:
    doc = xmltodict.parse(fd.read())

datas = doc['soap:Envelope']['soap:Body']['showResponse']['showResult']['diffgr:diffgram']['NewDataSet']['Table']

header = [ 'State', 'District', 'Market', 'Commodity', 'Variety', 'Arrival_Date', 'Min_x0020_Price', 'Max_x0020_Price', 'Modal_x0020_Price' ]
values = []
values.append(header)
for datapoint in datas:
    value = []
    for key in header:
        value.append(datapoint[key])
    values.append(value)

oname = fname.replace('.xml','.tsv')
with open(oname,'w') as f:
    odata = [ '\t'.join(x) for x in values ]
    odata = '\n'.join(odata)
    f.write(odata)
