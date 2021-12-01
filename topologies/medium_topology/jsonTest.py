import json
# Import the os module
import os
import string
import ipaddress

def file_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    new_path = os.path.join(dir, *split_path)
    return new_path

def getFirstKeyOfDict(dataDict:dict):
    return list(dataDict.keys())[0]

with open(file_path("/addressConfiguration.json"), "r") as addressFile:
            data = json.load(addressFile)

# with open(file_path("conf/r1zebra.conf"), "r") as template:
#     print(template.read())
routers = {}
for index,router in enumerate(data["routers"]):
    interfaces = data["routers"][router]["interfaces"]["real"]
    routers["router" + str(index+1)] = interfaces[getFirstKeyOfDict(interfaces)]
    print(interfaces)
# for index,firstInterface in enumerate(data["links"]):
#     firstRouter = firstInterface.rpartition('-')[0]
#     secondInterface = data["links"][firstInterface]
#     secondRouter = secondInterface.rpartition('-')[0]


# with open(file_path("/config_templates/zebra_template.conf"), "r") as template:
#     zebraTemplate = template.read()
# print(zebraTemplate)
# routers = []
# for index,router in enumerate(data["routers"]):
#     routers.append(router)
#     with open(file_path(f'/conf/{router}zebra.conf'), 'w+') as filehandle:
#         filehandle.write(zebraTemplate)

# def getFirstKeyOfDict(dataDict:dict):
#     return list(dataDict.keys())[0]
# def getRouterFirstInterface(data:dict, router:str, withWildCard:bool):
#     interface = data["routers"][router]["interfaces"]["real"]
#     return interface[getFirstKeyOfDict(interface)] if withWildCard else removeWildCard(interface[getFirstKeyOfDict(interface)])

# def removeWildCard(ip:str):
#     return ip[:-3]

# def zeroLastDigit(ip:str):
#     index = ip.rindex(".")
#     return ip[:index+1] + "0"

# def getAllInterfacesOfRouter(data:dict, router:str, withWildCard:bool):
#     interface = data["routers"][router]["interfaces"]["real"]
#     addressList = []
#     for i in list(interface.keys()):
#         addressList.append(interface[i]) if withWildCard else addressList.append(removeWildCard(interface[i]))
#     return addressList

# print(getAllInterfacesOfRouter(data, "r1", True))
# with open(file_path("/config_templates/ospf_template.conf"), "r") as template:
#     zebraTemplate = string.Template(template.read())
#     networkCommand = ""
# for address in getAllInterfacesOfRouter(data, "r1", False):
#     print("!!!!!" + zeroLastDigit(address))
#     networkCommand += f"network {zeroLastDigit(address)}/24 area 0\n  "
#     confFile = zebraTemplate.safe_substitute(
#             id = getRouterFirstInterface(data, router, False),
#             network = networkCommand)
# print(confFile)
# routers = []

# for index,router in enumerate(data["routers"]):
#     routers.append(router)
#     with open(file_path(f'/conf/{router}zebra.conf'), 'w+') as filehandle:
#         filehandle.write(zebraTemplate)


# print(routers)
