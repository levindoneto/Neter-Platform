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
logging.basicConfig(level = logging.INFO)
parser = argparse.ArgumentParser(description = "Mininet Script")
parser.add_argument("--ip", action = "store", dest = "ip", default = DEFAULT_IP, required = False, help = "Controller IP")
net = None

"""
Create topology.
"""
def startNetwork(auto_set_macs, hosts, ip, links, switches):
    global net
    net = Mininet(topo = topology.topologyMininet(hosts, switches, links), build = False, autoSetMacs = auto_set_macs, controller = partial(RemoteController, ip = ip))
    #net.addController('c0') # To let the controller in the local mode
    closeNetwork()
    logger.info("\nStarting network,\nNET:")
    logger.info(net)
    logger.info("- Hosts: %s" % str(hosts))
    logger.info("- Switches: %s" % str(switches))
    logger.info("- Links: %s" % str(links))
    logger.info("- RemoteController: %s" % str(ip))
    #try:
    net.start() # Init the network
    logger.info("Network started")
    #logger.error("On starting network")
    return True

"""
Ping all devices.
"""
def pingAll():
    logger.info("\nPinging network,\nNET:")
    logger.info(net)
    try:
        net.pingAll()
    except:
        logger.error("On pinging network")
    return True

"""
Get active hosts' ips.
"""
def getHosts():
    hosts = dict()
    logger.info("\nGetting hosts")
    try:
        for host in net.hosts:
            hosts.update({str(host):host.IP()})
        logger.info("Hosts: %s" % str(hosts))
    except:
        logger.error("On getting hosts")
    return hosts

"""
Stop current network.
"""
def stopNetwork():
    logger.info("\nStoping network")
    try:
        net.stop()
    except:
        logger.error("On stoping network")
    return True

"""
Stop mininet.
"""
def closeNetwork():
    logger.info("Closing network")
    try:
        import os
        os.system("sudo mn -c")
    except:
        logger.error("On closing network")
    return True
