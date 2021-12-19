#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time
import os
import json
import string

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter "

    def build( self, **_opts ):

        data = getConfigFromJson(file_path("/addressConfiguration.json"))
        routers = {}
        routers = addRoutersToGraph(self,data)    
        host =""
        h1 = self.addHost( 'h1', ip=self.getHostIp(data, "h1"), defaultRoute=self.getHostDefaultRoute(data, "h1")) #define gateway
        h2 = self.addHost( 'h2', ip=self.getHostIp(data, "h2"), defaultRoute=self.getHostDefaultRoute(data, "h2"))

        

        s1 = self.addSwitch("s1", cls=OVSSwitch)
        s2 = self.addSwitch("s2", cls=OVSSwitch)

        self.linkRoutersWithHosts(data)

        addLinkBwRouters(self, data, routers)

    def getHostDefaultRoute(self, data, host):
        return f'via ${data["hosts"][host]["defaultRoute"]}'

    def getHostIp(self, data, host):
        return data["hosts"][host]["interfaces"]["ip"]

    def linkRoutersWithHosts(self, data):
        info("hoost \n")
        links = {}
        for key,value in data["links"].items():
            if value[0].lower() == "h":
                links[key] = value 
        for interface, host in links.items():
            router = interface.rpartition('-')[0]
            self.addLink(host,router,intfName2=interface)

def addLinkBwRouters(self, data: dict, routers: dict):
    for firstInterface in data["links"]:
        secondInterface = data["links"][firstInterface]
        secondRouter = secondInterface.rpartition('-')[0]
        if(secondInterface.lower()[0] == "r"):
            firstRouter = firstInterface.rpartition('-')[0]
            firstIp = getIpOfInterface(data, firstInterface, firstRouter)
            secondIp = getIpOfInterface(data, secondInterface, secondRouter)
            linkRouterWithRouter(self, firstInterface, firstRouter, secondInterface, secondRouter, firstIp, secondIp)
        elif (secondInterface.lower()[0] == "s"):
            firstRouter = firstInterface.rpartition('-')[0]
            firstIp = getIpOfInterface(data, firstInterface, firstRouter)
            linkRouterWithSwitch(self, firstRouter, secondInterface, firstInterface, firstIp)
        elif (secondInterface.lower()[0] == "h"):
            pass


def linkRouterWithSwitch(self, router, switch, routerInterface, firstIp):
    info("link r with sw "+ router + switch + routerInterface + firstIp +"\n")
    self.addLink(router, switch, 
            intfName1=routerInterface,
            params1={ 'ip':firstIp })

def linkRouterWithRouter(self, firstInterface, firstRouter, secondInterface, secondRouter, firstIp, secondIp):
    self.addLink(firstRouter,secondRouter,
            intfName1=firstInterface,intfName2=secondInterface,
            params1={ 'ip':firstIp }, params2 = { 'ip':secondIp} )


def getIpOfInterface(data, interface, router):
    return data["routers"][router]["interfaces"]["real"][interface]

def getConfigFromJson(path):
    with open(path, "r") as addressFile:
        data = json.load(addressFile)
    return data
        

def addRoutersToGraph(self, data: dict):
    routers = {}
    for index,router in enumerate(data["routers"]):
        interface = data["routers"][router]["interfaces"]["real"]
        routers[router] = self.addNode(
                router, cls=LinuxRouter,
                 ip=interface[getFirstKeyOfDict(interface)]
                 )
    return routers

def getFirstKeyOfDict(dataDict:dict):
    return list(dataDict.keys())[0]
    
def addAliasToInterface(interface: str, addressWithMask: str):
    # interface such as r1-eth1:0
    # addressWithMask such as 10.0.3.11/24
    return f'ifconfig {interface} {addressWithMask} \n'


def file_path(relative_path):
    # get correct absolute path for given file
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    new_path = os.path.join(dir, *split_path)
    return new_path

def getRouterNames(data:dict):
    routers = []
    for index,router in enumerate(data["routers"]):
        routers.append(router)
    return routers

def loadZebraForAllRouters(net:Mininet, data:dict):
    routers = getRouterNames(data)
    for r in routers:
        device=net.getNodeByName(r)
        device.cmd(f'zebra -f conf/{r}zebra.conf -d -z ~/{r}zebra.api -i ~/{r}zebra.interface')

def loadOspfForAllRouters(net:Mininet, data:dict):
    routers = getRouterNames(data)
    for r in routers:
        device=net.getNodeByName(r)
        device.cmd(f'ospfd -f conf/{r}ospfd.conf -d -z ~/{r}zebra.api -i ~/{r}ospfd.interface')

def getTemplateOf(templateName:str):
    with open(file_path(f"/config_templates/{templateName}"), "r") as file:
        template = string.Template(file.read())
    return template

def generateZebraConfFIles(data:dict):
    zebraTemplate = getTemplateOf("zebra_template.conf").safe_substitute()
    routers = getRouterNames(data)
    for router in routers:
        with open(file_path(f'/conf/{router}zebra.conf'), 'w+') as filehandle:
            filehandle.write(zebraTemplate)

def getRouterFirstInterface(data:dict, router:str, withWildCard:bool):
    interface = data["routers"][router]["interfaces"]["real"]
    return interface[getFirstKeyOfDict(interface)] if withWildCard else removeWildCard(interface[getFirstKeyOfDict(interface)])

def getAllInterfacesOfRouter(data:dict, router:str, withWildCard:bool):
    interface = data["routers"][router]["interfaces"]["real"]
    addressList = []
    for i in list(interface.keys()):
        addressList.append(interface[i]) if withWildCard else addressList.append(removeWildCard(interface[i]))
    return addressList

def removeWildCard(ip:str):
    return ip[:-3]

def zeroLastDigit(ip:str):
    index = ip.rindex(".")
    return ip[:index+1] + "0"

def generateOspfConfFiles(data:dict):
    routers = getRouterNames(data)
    ospfTemplate = getTemplateOf("ospf_template.conf")
    for router in routers:
        networkCommand = ""
        for address in getAllInterfacesOfRouter(data, router, True):
            networkCommand += f"network {zeroLastDigit(address)}/24 area 0\n  "
        confFile = ospfTemplate.safe_substitute(
            name = f'{router}_ospf',
            id = getRouterFirstInterface(data, router, False),
            network = networkCommand)
        with open(file_path(f'/conf/{router}ospfd.conf'), 'w+') as filehandle:
            filehandle.write(confFile)
        

def run():
    "Test linux router"
    topo = NetworkTopo()
    # add controller
    c0 = RemoteController('remoteController', ip = '192.168.1.78', port = 6653)
    net = Mininet(topo=topo , build=False, waitConnected=True, controller=RemoteController)  
    net.addController(c0)

    net.build()
    net.start()
    
    data = getConfigFromJson(file_path("/addressConfiguration.json"))


    info('*** Starting switches, note: switch names must start with "s" and host must connect to r#-eth0\n')
    for sw in ["s1", "s2"]:
        net.get(sw).start([c0])

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    
    generateZebraConfFIles(data)
    generateOspfConfFiles(data)
    loadZebraForAllRouters(net, data)
    loadOspfForAllRouters(net, data)

      
    CLI( net )
    net.stop()
    os.system("killall -9 ospfd zebra")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

