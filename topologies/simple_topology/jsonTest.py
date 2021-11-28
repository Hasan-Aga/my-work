import json
# Import the os module
import os

def file_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    print(dir)
    split_path = relative_path.split("/")
    print(split_path)
    new_path = os.path.join(dir, *split_path)
    print(new_path)
    return new_path


with open(file_path("/addressConfiguration.json"), "r") as addressFile:
            data = json.load(addressFile)

routers = {}
for index,router in enumerate(data):
    routers["router" + str(index+1)] = data[router]["interfaces"]["real"]["defaultIP"]

print(routers)
