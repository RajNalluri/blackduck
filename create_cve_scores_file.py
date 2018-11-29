import json
import os
import requests
import zipfile

def downloadZips():
    # download zips to "downloads" folder
    url = "https://nvd.nist.gov/feeds/json/cve/1.0/"
    os.system("mkdir downloads28")
    os.chdir("downloads28")
    for year in range(2002,2019):
        print("Downloading "+str(year))
        r = requests.get(url+"nvdcve-1.0-"+str(year)+".json.zip")
        with open(str(year)+".zip", 'wb') as f:
            for chunk in r.iter_content(100000):
                f.write(chunk)

def extractjsons():
    # extract zips to "downloads/jsons" folder
    files = [f for f in os.listdir("downloads28/") if os.path.isfile(os.path.join("downloads28/", f))]
    files.sort()
    for file in files:
        zip_ref = zipfile.ZipFile(os.path.join("downloads28/", file), 'r')
        zip_ref.extractall("downloads28/jsons")
        zip_ref.close()

jsonfiles=[f for f in os.listdir("downloads28/jsons")]
print(jsonfiles)


g = open("final_mapping.csv", "w")
g.write("cve,cvssV3,cvssV2\n")


def cvssV3(di):
    try:
        return str(di["impact"]["baseMetricV3"]["cvssV3"]["baseScore"])
    except:
        return "NA"

def cvssV2(di):
    try:
        return str(di["impact"]["baseMetricV2"]["cvssV2"]["baseScore"])
    except:
        return "NA"

def create_mapping_file():
    for i in jsonfiles:
        f = open(os.path.join("downloads28/jsons",i), encoding='utf-8')
        data=json.load(f)
        # except Exception as e: print(e)

        for d in data["CVE_Items"]:
            g.write(d["cve"]["CVE_data_meta"]["ID"]+","+cvssV3(d)+","+cvssV2(d)+"\n")
        f.close()

create_mapping_file()
# downloadZips()
# extractjsons()