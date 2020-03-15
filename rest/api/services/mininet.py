#!/usr/bin/env python

import time
from models import topology
import argparse
from functools import partial # for using the RemoteController
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
from logging import Log

DEFAULT_IP = "127.0.0.1"

parser = argparse.ArgumentParser(description = "Mininet Script")
parser.add_argument("--ip", action = "store", dest = "ip", default = DEFAULT_IP, required = False, help = "Controller IP")
net = None
setLogLevel('info')

def startNetwork(auto_set_macs, hosts, ip, links, switches):
    net = Mininet(topo = topology.topologyMininet(hosts, switches, links), build = False, autoSetMacs = auto_set_macs, controller = partial(RemoteController, ip = ip))
    #net.addController('c0') # To let the controller in the local mode
    net.start() # Init the network
    return True

# Ping between all devices
def pingAll():  
    net.pingAll()
    return True

def getHosts():
    hosts = dict()
    for host in net.hosts:
        hosts.update({str(host):host.IP()})
    return hosts

def stopNetwork():
    net.stop()
    return True

def attackNetwork():
    for i in range(1, 5000):
        print(h3.cmd('ping -c1 %s' % h4.IP()))
    return True

def closeNetwork():
    import os
    os.system("sudo mn -c")
    return True