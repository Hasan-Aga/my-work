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


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    "A LinuxRouter "

    def build(self, **_opts):

        data = getConfigFromJson(file_path("/addressConfiguration.json"))
        routers = {}
        routers = addRoutersToGraph(self, data)

        h2 = self.addHost('h2', ip='10.0.8.100/24',
                          defaultRoute='via 10.0.8.1')
        # h1 = self.addHost('h1', ip='10.0.0.100/24',
        #                   defaultRoute='via 10.0.0.1')  # define gateway

        addLinkBwRouters(self, data, routers)

        # params2 define the eth2 ip address
        # self.addLink(h1, routers["r1"], intfName2='r1-eth0',
        #              params2={'ip': '10.0.0.1/24'})
        self.addLink(h2, routers["r4"], intfName2='r4-eth1',
                     params2={'ip': '10.0.8.1/24'})

# TODO fix wrong ip in r1 
#TODO look into addLink()
# https://mailman.stanford.edu/pipermail/mininet-discuss/2015-March/005895.html


def addLinkBwRouters(self, data: dict, routers: dict):
    info(str(data["links"]) + "\n")
    for firstInterface in data["links"]:
        firstRouter = firstInterface.rpartition('-')[0]
        info(firstRouter + "\n")
        addressOne = data["routers"][firstRouter]["interfaces"]["real"][firstInterface]
        secondInterface = data["links"][firstInterface]
        secondRouter = secondInterface.rpartition('-')[0]
        addressTwo = data["routers"][secondRouter]["interfaces"]["real"][secondInterface]
        info(firstRouter + " int. " +
             firstInterface + " ip = " + addressOne + "\n")
        info(secondRouter + " int. " +
             secondInterface + " ip = " + addressTwo + "\n")

        self.addLink(
            firstRouter, secondRouter,
            intfName1=firstInterface,params1={'ip': addressOne},
             intfName2=secondInterface, params2={'ip': addressTwo}
        )


def getConfigFromJson(path):
    with open(path, "r") as addressFile:
        data = json.load(addressFile)
    return data


def addRoutersToGraph(self, data: dict):
    routers = {}
    for index, router in enumerate(data["routers"]):
        interface = data["routers"][router]["interfaces"]["real"]
        routers[router] = self.addNode(
            router, cls=LinuxRouter, ip=interface[getFirstKeyOfDict(interface)])
    return routers


def getFirstKeyOfDict(dataDict: dict):
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


def getRouterNames(data: dict):
    routers = []
    for index, router in enumerate(data["routers"]):
        routers.append(router)
    return routers


def loadZebraForAllRouters(net: Mininet, data: dict):
    routers = getRouterNames(data)
    for r in routers:
        device = net.getNodeByName(r)
        device.cmd(
            f'zebra -f conf/{r}zebra.conf -d -z ~/{r}zebra.api -i ~/{r}zebra.interface')


def loadOspfForAllRouters(net: Mininet, data: dict):
    routers = getRouterNames(data)
    for r in routers:
        device = net.getNodeByName(r)
        device.cmd(
            f'ospfd -f conf/{r}ospfd.conf -d -z ~/{r}zebra.api -i ~/{r}ospfd.interface')


def getTemplateOf(templateName: str):
    with open(file_path(f"/config_templates/{templateName}"), "r") as file:
        template = string.Template(file.read())
    return template


def generateZebraConfFIles(data: dict):
    zebraTemplate = getTemplateOf("zebra_template.conf").safe_substitute()
    routers = getRouterNames(data)
    for router in routers:
        with open(file_path(f'/conf/{router}zebra.conf'), 'w+') as filehandle:
            filehandle.write(zebraTemplate)


def getRouterFirstInterface(data: dict, router: str, withWildCard: bool):
    interface = data["routers"][router]["interfaces"]["real"]
    return interface[getFirstKeyOfDict(interface)] if withWildCard else removeWildCard(interface[getFirstKeyOfDict(interface)])


def getAllInterfacesOfRouter(data: dict, router: str, withWildCard: bool):
    interface = data["routers"][router]["interfaces"]["real"]
    addressList = []
    for i in list(interface.keys()):
        addressList.append(interface[i]) if withWildCard else addressList.append(
            removeWildCard(interface[i]))
    return addressList


def removeWildCard(ip: str):
    return ip[:-3]


def zeroLastDigit(ip: str):
    index = ip.rindex(".")
    return ip[:index+1] + "0"


def generateOspfConfFiles(data: dict):
    routers = getRouterNames(data)
    ospfTemplate = getTemplateOf("ospf_template.conf")
    for router in routers:
        networkCommand = ""
        for address in getAllInterfacesOfRouter(data, router, True):
            networkCommand += f"network {zeroLastDigit(address)}/24 area 0\n  "
        confFile = ospfTemplate.safe_substitute(
            name=f'{router}_ospf',
            id=getRouterFirstInterface(data, router, False),
            network=networkCommand)
        with open(file_path(f'/conf/{router}ospfd.conf'), 'w+') as filehandle:
            filehandle.write(confFile)

# TODO on the VM, remove old conf and use new ones
# TODO clean folders and improve readmes


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(controller=None, topo=topo)  # controller is used by s1-s3
    # info("type of net = " + str(type(net)) + " \n")
    net.start()

    data = getConfigFromJson(file_path("/addressConfiguration.json"))
    generateZebraConfFIles(data)
    generateOspfConfFiles(data)
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

    CLI(net)
    net.stop()
    os.system("killall -9 ospfd zebra")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")


if __name__ == '__main__':
    setLogLevel('info')
    run()
