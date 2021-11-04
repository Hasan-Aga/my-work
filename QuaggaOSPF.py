from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time
import os

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

    def build( self, **_opts):
        defaultIP1 = '10.0.3.10/24'  # IP address for r0-eth1
        defaultIP2 = '10.0.3.20/24' 
        router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1 )
	    router2 = self.addNode( 'r2', cls=LinuxRouter, ip=defaultIP2 )

        h1 = self.addHost( 'h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.10') #define gateway
        h2 = self.addHost( 'h2', ip='10.0.2.100/24', defaultRoute='via 10.0.2.20')

        self.addLink(router1,router2,intfName1='r1-eth1',intfName2='r2-eth1')
	    self.addLink(h1,router1,intfName2='r1-eth2',params2={ 'ip' : '10.0.1.10/24' })#params2 define the eth2 ip address
	    self.addLink(h2,router2,intfName2='r2-eth2',params2={ 'ip' : '10.0.2.20/24' })