
from htmlParser import MyHTMLParser
import pprint
import requests
import re
import json
import os, sys

def getDbGapVarId(study_id,variable_id):
    response = requests.get("https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/variable.cgi?study_id="+study_id+"&phv="+variable_id)
    # print(response.text)
    matchVariable = re.search("(phv[0-9]+\\.v[0-9]+\\.p[0-9]+)", response.text)
    matchDataSet = re.search("(pht[0-9]+\\.v[0-9]+\\.p[0-9]+)", response.text)
    # print(match)

    if matchVariable:
        dataSet = matchDataSet.group(1)
    variable = matchVariable.group(1)
    if matchDataSet:
        print('dataset', matchDataSet.group(1))
        print('variable', matchVariable.group(1))
    return dataSet, variable

def parse(init_study_id, init_current_type, init_current_object_id, init_current_folder_type,leafs,fileNum,study_id):
    fileNum += 1
    url = \
        'https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/' + \
        'GetFolderView.cgi?current_study_id=' + init_study_id + \
        '&current_type=' + str(init_current_type) + \
        '&current_object_id=' + str(init_current_object_id) + \
        '&current_folder_type=' + str(init_current_folder_type)
    print(url)
    try:
        response = requests.get(url)
        parser = MyHTMLParser()
        parser.groupNodes = []
        parser.leafs = []
        parser.feed(response.text)
        # pprint.pprint(response.text)
        # pprint.pprint(parser.groupNodes)
        pprint.pprint(parser.leafs)
        groupNodes = parser.groupNodes
        leafs.extend(parser.leafs)
        leafsDef = {}
        print("exists" + leafFilePath + "-"+str(init_current_object_id), os.path.exists(leafFilePath + "-"+str(init_current_object_id)))
        if not os.path.exists(leafFilePath + "-"+str(init_current_object_id)):
            for leaf in leafs:
                print(leaf)
                try:
                    dataSet, variable = getDbGapVarId(study_id, leaf.get('phv'))
                    varIdentifier = study_id.split(".")[0]+"."+study_id.split(".")[1]+"."+dataSet+"."+variable.split(".")[0]+"."+variable.split(".")[1]
                    leafDef = {
                        "var": leaf.get('var'),
                        "path":  leaf.get('path'),
                        "phv":  leaf.get('phv'),
                        "varIdentifier": varIdentifier
                    }
                    leafsDef[varIdentifier] = leafDef
                except:
                    print("ERROR", "URL NOT RESPONDING ==>",study_id, leaf.get('phv'))
            print("leafsDef", bool(leafsDef),init_current_object_id)
            if bool(leafsDef):
                with open(leafFilePath + "-"+str(init_current_object_id), 'w') as outfile:
                    json.dump(leafsDef, outfile)
                    outfile.close()
            # pprint.pprint(leafs)
        print(groupNodes)
        for groupNode in groupNodes:
            print(url , groupNode)
            study_id = groupNode.split(', ')[0].replace("'","").strip()
            # print('current_object_upNode.split(', ')[0].replace("'","").strip()
            current_type = groupNode.split(', ')[1].strip()
            current_object_id = groupNode.split(', ')[2].strip()
            current_folder_type = groupNode.split(', ')[3].strip()
            print('current_object_id ', current_object_id)
            leafs = []
            parse(study_id, current_type, current_object_id, current_folder_type,leafs,fileNum,study_id)
            # print('leafs ' , leafs)
    except:
        print("ERROR", "URL NOT RESPONDING ==>",url )

with open('./properties.json') as json_data:
    #  Read property file
    data = json.load(json_data)
    study_id = data.get('study_id')
    current_object_id = data.get('current_object_id')
    retrievePaths = data.get("retrievePaths")
    buildMappingFile = data.get("buildMappingFile")
    leafFilePath = data.get("leafFilePath")
    sourceMappingFile = data.get("sourceMappingFile")
    targetMappingFile = data.get("targetMappingFile")

    # set default param for intitialization
    current_type = 0
    current_folder_type = 102
    leafs = []

    fileNum = 0
    print("---------------------------")
    print("Checking directories")

    if(retrievePaths == "Y"):
        print(" - " +  os.path.dirname(leafFilePath) + " - " + str(os.path.exists(os.path.dirname(leafFilePath))))
        if not os.path.exists(os.path.dirname(leafFilePath)):
            print(leafFilePath, "Does not exists - Stopping")
            sys.exit("[ERROR] "+ leafFilePath + " Does not exists - Stopped")

    if(buildMappingFile == "Y"):
        print(" - " + sourceMappingFile  + " - " + str(os.path.exists(sourceMappingFile)))
        if not os.path.exists(sourceMappingFile):
            print(sourceMappingFile, "Does not exists - Stopping")
            sys.exit("[ERROR] "+sourceMappingFile + " Does not exists - Stopped")

        print(" - " +  os.path.dirname(targetMappingFile) + " - " + str(os.path.exists(os.path.dirname(targetMappingFile))))
        if not os.path.exists(os.path.dirname(targetMappingFile)):
            print(targetMappingFile, "Does not exists - Stopping")
            sys.exit("[ERROR] "+targetMappingFile + " Does not exists - Stopped")

    if(retrievePaths == "Y"):
            parse(study_id, current_type, current_object_id, current_folder_type, leafs,fileNum,leafFilePath)
            leafsDef = {}
            for file in os.listdir(os.path.dirname(leafFilePath)):
                if re.match(os.path.basename(leafFilePath) + "-[0-9]+",file):
                    print(file)
                    with open(os.path.dirname(leafFilePath)+"/"+file) as json_data:
                        data = json.load(json_data)
                        leafsDef.update(data)
            with open(leafFilePath, 'w') as outfile:
                json.dump(leafsDef, outfile)
                outfile.close()
            # for leaf in leafs
            #     print(leaf)
            #     try:
            #         dataSet, variable = getDbGapVarId(study_id, leaf.get('phv'))
            #         varIdentifier = study_id.split(".")[0]+"."+study_id.split(".")[1]+"."+dataSet+"."+variable.split(".")[0]+"."+variable.split(".")[1]
            #         leafDef = {
            #             "var": leaf.get('var'),
            #             "path":  leaf.get('path'),
            #             "phv":  leaf.get('phv'),
            #             "varIdentifier": varIdentifier
            #         }
            #         leafsDef[varIdentifier] = leafDef
            #     except:
            #         print("ERROR", "URL NOT RESPONDING ==>",study_id, leaf.get('phv'))



    if(buildMappingFile == "Y"):
        with open(targetMappingFile, 'w') as targetMapping:
            with open(leafFilePath) as leafsFile:
                leafs = json.load(leafsFile)
            with open(sourceMappingFile, 'r') as mappingSource:
                lines = mappingSource.readlines()
                mappingSource.close()
            n = 0
            for line in lines:
                data = line.split(",")
                if n == 0:
                    h = 0
                    for head in data:
                        print(head)
                        if head.strip() == "varIdentifier":
                            keyIndex = h
                            break
                        h += 1
                else:
                    varIdentifier = data[keyIndex].replace('"', '').strip()
                    oldPath = data[1]
                    labelVar = data[1].split("\\")[-2]
                    # print('oldPath', oldPath)
                    # print('labelVar', labelVar)
                    # print(varIdentifier)
                    if varIdentifier in leafs:
                        # pprint.pprint(leafs[varIdentifier])
                        newPath = leafs[varIdentifier].get("path")+"\\"+labelVar+"\\"
                        # print('newPath', newPath)
                        line = line.replace(oldPath, newPath)
                        # print(line)
                targetMapping.write(line)
                n += 1
