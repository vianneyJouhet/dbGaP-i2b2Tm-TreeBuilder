from HTMLParser import HTMLParser
import re


class MyHTMLParser(HTMLParser):
    groupNodes = []
    leafs = []
    buildPath = True
    addToPath = False
    addDataPath = False
    addRoot = False
    checkNode = False
    groupNode = False
    leaf = False
    path = ""
    varId = ""

    def handle_starttag(self, tag, attrs):
        if (tag == "hr"):
            self.checkNode = True
            self.buildPath = False
        else:
            if(tag == "a" and self.groupNode is False):
                self.leaf = True

            for attr in attrs:
                if(attr[0] == "class" and attr[1] == "studyNode" and self.buildPath):
                    self.addToPath = True
                if(self.buildPath and attr[0] == "class" and attr[1] == "groupNode"):
                    self.addToPath = True
                if(self.checkNode and attr[0] == "class" and attr[1] == "groupNode"):
                    self.groupNode = True
                if (attr[0] == "onclick" and self.groupNode):
                    match = re.search("updateAssociatedBox\\(([^\\)]*)\\)", attr[1])
                    self.groupNodes.append(match.group(1))
                if (self.leaf and attr[0] == "onclick"):
                    print(attr[1])
                    matchVarId = re.search("([0-9]+)",attr[1])
                    self.varId=matchVarId.group(1)
    def handle_endtag(self, tag):
        # print("Encountered end tag  :", tag)
        if(self.groupNode and tag == "div"):
            self.groupNode = False

    def handle_data(self, data):

        if self.addRoot:
            self.addRoot = False
        if self.leaf:
            self.leaf = False
            newPath = {
                "var": data,
                "path": self.path,
                "phv": self.varId
            }
            self.leafs.append(newPath)
            print(newPath)
        if self.addToPath:
            self.addToPath = False
            self.path += "\\" + data.replace(";", ".").replace(",", " ").replace("\"", "").replace("\n", " ").replace("\\","/")
            print(data)
