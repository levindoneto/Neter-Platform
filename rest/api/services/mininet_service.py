#!/usr/bin/env python

import time
from models import topology
import argparse
from functools import partial # for using the RemoteController
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
import logging

DEFAULT_IP = "127.0.0.1"
logger = logging.getLogger("mininet")
parser = argparse.ArgumentParser(description = "Mininet Script")
parser.add_argument("--ip", action = "store", dest = "ip", default = DEFAULT_IP, required = False, help = "Controller IP")
net = None

def startNetwork(auto_set_macs, hosts, ip, links, switches):
    net = Mininet(topo = topology.topologyMininet(hosts, switches, links), build = False, autoSetMacs = auto_set_macs, controller = partial(RemoteController, ip = ip))
    #net.addController('c0') # To let the controller in the local mode
    logger.info("Starting network")
    logger.info("- Hosts: %s" % str(hosts))
    logger.info("- Switches: %s" % switches)
    try:
        net.start() # Init the network
    except:
        logger.error("On starting network")
    return True

# Ping all devices
def pingAll():
    logger.info("Pinging network")
    try:
        net.pingAll()
    except:
        logger.error("On pinging network")
    return True

def getHosts():
    hosts = dict()
    logger.info("Getting hosts")
    try:
        for host in net.hosts:
            hosts.update({str(host):host.IP()})
        logger.info("Hosts: %s" % str(hosts))
    except:
        logger.error("On getting hosts")
    return hosts

def stopNetwork():
    logger.info("Stoping network")
    try:
        net.stop()
    except:
        logger.error("On stoping network")
    return True

def attackNetwork(level=5000):
    logger.info("Attacking network with level %s " % str(level))
    try: 
        hosts = net.hosts
        for i in range(1, level):
            print(hosts[0].cmd('ping -c1 %s' % hosts[0].IP()))
    except:
        logger.error("On attacking network")
    return True

def closeNetwork():
    logger.info("Closing network")
    try:
        import os
        os.system("sudo mn -c")
    except:
        logger.error("On closing network")
    return True
