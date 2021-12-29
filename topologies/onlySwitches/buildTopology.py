from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class SwitchTopo(Topo):
    "topology using only switches for routing"
    def build( self, **_opts ):
        
        s1 = self.addSwitch("s1", cls=OVSSwitch, protocols="OpenFlow13")
        s2 = self.addSwitch("s2", cls=OVSSwitch, protocols="OpenFlow13")
        s3 = self.addSwitch("s3", cls=OVSSwitch, protocols="OpenFlow13")
        s4 = self.addSwitch("s4", cls=OVSSwitch, protocols="OpenFlow13")