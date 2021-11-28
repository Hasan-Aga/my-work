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

hosts = {}
for index,host in enumerate(data["hosts"]):
    interface = data["hosts"][host]["defaultRoute"]
    print("interface=" + interface[:2])
    hosts["h" + str(index+1)] = f'via {data["routers"][interface[:2]]["interfaces"]["real"][interface]}'

print(hosts)
