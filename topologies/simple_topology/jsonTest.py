import json
# Import the os module
import os

def file_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    new_path = os.path.join(dir, *split_path)
    return new_path


with open(file_path("/addressConfiguration.json"), "r") as addressFile:
            data = json.load(addressFile)

routers = {}
for index,router in enumerate(data["routers"]):
    routers["router" + str(index+1)] = data["routers"][router]["interfaces"]["real"]["defaultIP"]

for index,firstInterface in enumerate(data["links"]):
    firstRouter = firstInterface.rpartition('-')[0]
    secondInterface = data["links"][firstInterface]
    secondRouter = secondInterface.rpartition('-')[0]
    print(firstRouter, firstInterface, secondInterface, secondRouter)

