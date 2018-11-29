from pandas import read_csv
from version_utils import rpm
from pymongo import MongoClient
import os
import json
import sys


class SecuritySheet:
    # def __init__(self, securitycsv):
    def create_cvejson(self):
        cvedict_cmd = "sqlite3 < cvedict_command.txt"
        os.system(cvedict_cmd)

        df = read_csv('cvedict.csv')
        cvejson = {}
        for index, row in df.iterrows():
            cvejson[str(row["Vulnerability id"])] = {"score": str(row["Base score"]),
                                                     "description": str(row["Description"]),
                                                     "published_date": str(row["Published on"])}
        return cvejson

    def create_libjson(self):
        libdict_cmd = "sqlite3 < libdict_command.txt"
        os.system(libdict_cmd)

        cvejson = self.create_cvejson()

        df = read_csv('libdict.csv')
        libjson = {}
        for index, row in df.iterrows():
            libjson[str(row["Component name"])] = {}

        for index, row in df.iterrows():
            libjson[str(row["Component name"])][str(row["Component version name"])] = {}

        for index, row in df.iterrows():
            libjson[str(row["Component name"])][str(row["Component version name"])][str(row["Vulnerability id"])] = \
            cvejson[str(row["Vulnerability id"])]

        return libjson

class SourceSheet:
    def create_pathjson(self):
        rpmpath_cmd = "sqlite3 < rpmpathdict_command.txt"
        os.system(rpmpath_cmd)

        df = read_csv('pathdict.csv')

        pathjson = {}
        for index, row in df.iterrows():
            pathjson[str(row["rpm_name"])] = {}

        for index, row in df.iterrows():
            pathjson[str(row["rpm_name"])][str(row["Component name"])] = {}

        pathlist = []
        for index, row in df.iterrows():
            pathjson[str(row["rpm_name"])][str(row["Component name"])][str(row["Component version name"])] = []

        for index, row in df.iterrows():
            pathjson[str(row["rpm_name"])][str(row["Component name"])][str(row["Component version name"])].append(
                str(row["rpm_path"]).rstrip('/') + str(row["Path"]))
        return pathjson

class SourceSecurity:
    def create_finaljson(self):
        ssclub_cmd = "sqlite3 < ssclubdict_command.txt"
        os.system(ssclub_cmd)
        
        df = read_csv('ssclub.csv')

        rpmparsejson = {}
        for index, row in df.iterrows():
            try:
                rpmparsejson[str(row["rpm_name"])] = rpm.package(str(row["rpm_name"])).name
            except:
                rpmparsejson[str(row["rpm_name"])] = str(row["rpm_name"])

        sec = SecuritySheet()
        libjson = sec.create_libjson()

        source = SourceSheet()
        pathjson = source.create_pathjson()

        finaljson = {}
        for index, row in df.iterrows():
            finaljson[rpmparsejson[str(row["rpm_name"])]] = {"rpm_name": str(row["rpm_name"]), "details": []}

        for index, row in df.iterrows():
            finaljson[rpmparsejson[str(row["rpm_name"])]]["details"].append(
                {"lib": str(row["Component name"]), "libver": str(row["Component version name"]),
                 "cvelist": libjson[str(row["Component name"])][str(row["Component version name"])],
                 "pathlist": pathjson[str(row["rpm_name"])][str(row["Component name"])][
                     str(row["Component version name"])]})
        return finaljson

def create_mongo_collection(db="blackduck",col="blackduck_col"):
    ss = SourceSecurity()
    finaljson = ss.create_finaljson()

    client = MongoClient("127.0.0.1:27017")

    if db in client.list_database_names():
        print("database '%s' exists" % db)
        print("dropping database '%s'" % db)
        client.drop_database(db)

    bd_database = client[db]
    bd_collection = bd_database[col]

    mongo_id_list = []
    for each in finaljson:
        mongo_id_list.append(bd_collection.insert_one(finaljson[each]))
    # print(mongo_id_list)
    print(len(mongo_id_list), "documents are written to", "'"+ db +"'", "database as", "'" + col + "'", "collection!")

if __name__ == "__main__":
    # create_mongo_collection()
    ssobject = SourceSecurity()
    fjson = ssobject.create_finaljson()

    f = open('finaljson.json','w')
    f.write(json.dumps(fjson))