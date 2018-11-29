from pandas import read_csv
import json
import os

list_bd_cves = "sqlite3 < list_bd_cves.txt"
os.system(list_bd_cves)

input_to_final_score = "sqlite3 < input_to_finalscore.txt"
os.system(input_to_final_score)

df = read_csv('input_to_finalscore.csv')
scorejson = {}
for index, row in df.iterrows():
    scorejson[str(row["Vulnerability id"])] = {"bdscore": str(row["Base score"]),
                                             "cvssV2": str(row["cvssV2"]),
                                             "cvssV3": str(row["cvssV3"])}

# h = open("scorejson.json", "w")
# h.write(json.dumps(scorejson))
# h.close()

g= open('finalscores.csv','w')
g.write('Vulnerability id,bdscore,cvssV2,cvssV3,finalscore,severity\n')


def sev(s):
    if 9 <= float(s) <= 10: return 'critical'
    elif 7 <= float(s) <= 8.9: return 'major'
    elif 4 <= float(s) <= 6.9: return 'moderate'
    elif 0 <= float(s) <= 3.9: return 'minor'

def finalscore(di):
    if scorejson[di]['cvssV3'] != "nan":
        print(scorejson[di]['cvssV3']+','+sev(scorejson[di]['cvssV3']))
        return scorejson[di]['cvssV3']+','+sev(scorejson[di]['cvssV3'])
    elif scorejson[di]['cvssV2'] != "nan":
        print(scorejson[di]['cvssV2']+','+sev(scorejson[di]['cvssV2']))
        return scorejson[di]['cvssV2']+','+sev(scorejson[di]['cvssV2'])
    elif scorejson[di]['bdscore'] != "nan":
        print(scorejson[di]['bdscore']+','+sev(scorejson[di]['bdscore']))
        return scorejson[di]['bdscore']+','+sev(scorejson[di]['bdscore'])



for each in scorejson:
    print(each)
    g.write(each+','+ scorejson[each]['bdscore'] + ',' + scorejson[each]['cvssV2'] + ',' + scorejson[each]['cvssV3'] + ',' + finalscore(each)+'\n')

g.close()

new_security_file = "sqlite3 < new_security_file.txt"
os.system(new_security_file)