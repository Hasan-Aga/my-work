import json
# Import the os module
import os

def file_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    new_path = os.path.join(dir, *split_path)
    return new_path

def getFirstKeyOfDict(dataDict:dict):
    return list(dataDict.keys())[0]

with open(file_path("/addressConfiguration.json"), "r") as addressFile:
            data = json.load(addressFile)

routers = {}
for index,router in enumerate(data["routers"]):
    interfaces = data["routers"][router]["interfaces"]["real"]
    routers["router" + str(index+1)] = interfaces[getFirstKeyOfDict(interfaces)]

for index,firstInterface in enumerate(data["links"]):
    firstRouter = firstInterface.rpartition('-')[0]
    secondInterface = data["links"][firstInterface]
    secondRouter = secondInterface.rpartition('-')[0]


with open(file_path("/config_templates/zebra_template.conf"), "r") as template:
    zebraTemplate = template.read()
print(zebraTemplate)
routers = []
for index,router in enumerate(data["routers"]):
    routers.append(router)
    filehandle = open(file_path(f'/conf/{router}zebra.conf'), 'w+')
    filehandle.write(zebraTemplate)
    filehandle.close()

print(routers)
