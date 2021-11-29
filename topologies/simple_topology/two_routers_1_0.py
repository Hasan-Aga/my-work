#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
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
    "A LinuxRouter connecting three IP subnets"
    "The connection between routers uses IP aliases"

    def build( self, **_opts ):

        data = getConfigFromJson(file_path("/addressConfiguration.json"))
        routers = {}
        routers = addRoutersToGraph(self,data)
        
            
        h1 = self.addHost( 'h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.10') #define gateway
        h2 = self.addHost( 'h2', ip='10.0.2.100/24', defaultRoute='via 10.0.2.20')

        addLinkBwRouters(self, data, routers)

        self.addLink(h1,routers["r1"],intfName2='r1-eth2',params2={ 'ip' : '10.0.1.10/24' })#params2 define the eth2 ip address
        self.addLink(h2,routers["r2"],intfName2='r2-eth2',params2={ 'ip' : '10.0.2.20/24' })

def addLinkBwRouters(self, data: dict, routers: dict):
    for firstInterface in data["links"]:
        firstRouter = firstInterface.rpartition('-')[0]
        secondInterface = data["links"][firstInterface]
        secondRouter = secondInterface.rpartition('-')[0]
        self.addLink(firstRouter,secondRouter,intfName1=firstInterface,intfName2=secondInterface)


def getConfigFromJson(path):
    with open(path, "r") as addressFile:
        data = json.load(addressFile)
    return data
        
def addRoutersToGraph(self, data: dict):
    routers = {}
    for index,router in enumerate(data["routers"]):
        interface = data["routers"][router]["interfaces"]["real"]
        routers["r" + str(index+1)] = self.addNode( router, cls=LinuxRouter, ip=interface[getFirstKeyOfDict(interface)] )
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
        device.cmd(f'zebra -f /usr/local/etc/{r}zebra.conf -d -z ~/{r}zebra.api -i ~/{r}zebra.interface')

def loadOspfForAllRouters(net:Mininet, data:dict):
    routers = getRouterNames(data)
    for r in routers:
        device=net.getNodeByName(r)
        device.cmd(f'ospfd -f /usr/local/etc/{r}ospfd.conf -d -z ~/{r}zebra.api -i ~/{r}ospfd.interface')

def getTemplateOf(templateName:str):
    with open(file_path(f"/config_templates/{templateName}"), "r") as file:
        template = string.Template(file.read())
    return template

def generateZebraConfFIles(data:dict):
    zebraTemplate = getTemplateOf("zebra_template.conf")
    routers = getRouterNames(data)
    for r in routers:
        with open(file_path(f'/conf/{r}zebra.conf'), 'w+') as filehandle:
            filehandle.write(zebraTemplate)

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(controller = None, topo=topo )  # controller is used by s1-s3
    # info("type of net = " + str(type(net)) + " \n")
    net.start()
    
    data = getConfigFromJson(file_path("/addressConfiguration.json"))
    generateZebraConfFIles(data)
    loadZebraForAllRouters(net, data)
    loadOspfForAllRouters(net, data)

    
# TODO CONFIGURE ALIASING and generation of router conf files
    # info('configuring ip aliasing \n')
    # r1.cmd(addAliasToInterface('r1-eth1:0', '10.0.3.11/24'))
    # r1.cmd(addAliasToInterface('r2-eth1:0', '10.0.3.21/24'))

    # info('R1 interfaces: \n')
    # info( net[ 'r1' ].cmd( 'ifconfig' ) )
    # info('R2 interfaces: \n')
    # info( net[ 'r2' ].cmd( 'ifconfig' ) )



    # info('starting zebra and ospfd service:\n')
    # r1.cmd('zebra -f /usr/local/etc/r1zebra.conf -d -z ~/r1zebra.api -i ~/r1zebra.interface')
    # r2.cmd('zebra -f /usr/local/etc/r2zebra.conf -d -z ~/r2zebra.api -i ~/r2zebra.interface')
    # time.sleep(5) #time for zebra to create api socket
    # r1.cmd('ospfd -f /usr/local/etc/r1ospfd.conf -d -z ~/r1zebra.api -i ~/r1ospfd.interface')
    # r2.cmd('ospfd -f /usr/local/etc/r2ospfd.conf -d -z ~/r2zebra.api -i ~/r2ospfd.interface')
    
    
    CLI( net )
    net.stop()
    os.system("killall -9 ospfd zebra")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

