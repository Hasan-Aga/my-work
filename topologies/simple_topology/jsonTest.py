import json
# Import the os module
import os
import string

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


# with open(file_path("/config_templates/zebra_template.conf"), "r") as template:
#     zebraTemplate = template.read()
# print(zebraTemplate)
# routers = []
# for index,router in enumerate(data["routers"]):
#     routers.append(router)
#     with open(file_path(f'/conf/{router}zebra.conf'), 'w+') as filehandle:
#         filehandle.write(zebraTemplate)

def getFirstKeyOfDict(dataDict:dict):
    return list(dataDict.keys())[0]
def getRouterFirstInterface(data:dict, router:str, withWildCard:bool):
    interface = data["routers"][router]["interfaces"]["real"]
    return interface[getFirstKeyOfDict(interface)] if withWildCard else removeWildCard(interface[getFirstKeyOfDict(interface)])

def removeWildCard(ip:str):
    return ip[:-3]

with open(file_path("/config_templates/ospf_template.conf"), "r") as template:
    zebraTemplate = string.Template(template.read())
interface = data["routers"]["r1"]["interfaces"]["real"]
final = zebraTemplate.safe_substitute(id=getRouterFirstInterface(data,"r1",False))
print(final)
routers = []
# for index,router in enumerate(data["routers"]):
#     routers.append(router)
#     with open(file_path(f'/conf/{router}zebra.conf'), 'w+') as filehandle:
#         filehandle.write(zebraTemplate)


print(routers)
