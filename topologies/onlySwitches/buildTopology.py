from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class SwitchTopo(Topo):
    "topology using only switches for routing"
    def build( self, **_opts ):
        
        # Add switches
        s1 = self.addSwitch("s1", cls=OVSSwitch, protocols="OpenFlow13")
        s2 = self.addSwitch("s2", cls=OVSSwitch, protocols="OpenFlow13")
        s3 = self.addSwitch("s3", cls=OVSSwitch, protocols="OpenFlow13")
        s4 = self.addSwitch("s4", cls=OVSSwitch, protocols="OpenFlow13")

        # Add hosts 
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )

        # Add links
        self.addLink(leftHost, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(rightHost, s3)
        self.addLink(s3, s4)
        self.addLink(s4, s1)