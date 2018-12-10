from pandas import read_csv
import json

df = read_csv('affectedComponents.csv')
impactjson = {}
for index, row in df.iterrows():
    impactjson[str(row["Component"])] = []
for index, row in df.iterrows():
    impactjson[str(row["Component"])].append(str(row["Impacting library"]))
print(impactjson)

o = open("impactjson.json","w")
o.write(json.dumps(impactjson))
o.close()

i = open("outputfile.csv","w")
i.write("Component, Impacting Library\n")
for each in impactjson:
    i.write(each+","+"\""+str(impactjson[each]).strip("[").strip("]")+"\""+"\n")
