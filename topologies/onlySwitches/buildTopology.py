from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class SwitchTopo(Topo):
    "topology using only switches for routing"