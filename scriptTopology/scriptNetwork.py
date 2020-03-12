#!/usr/bin/env python

import time
import topology
import argparse
from functools import partial # for using the RemoteController

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
from os import system

parser = argparse.ArgumentParser(description = "Mininet Script")
parser.add_argument("--ip", action = "store", dest = "ip", default = "127.0.0.1", required = False, help = "Controller IP")

def menu():

    system("clear")

    print("|------------------------------------|")
    print("|------------- PLACIDUS -------------|")
    print("|------------------------------------|")
    print("|------- MININET TEST TOPOLOGY ------|")
    print("|------------------------------------|")
    print("| 1 - Init of topology test          |")
    print("| 2 - PingAll                        |")
    print("| 3 - See the IPs                    |")
    print("| 4 - Finalize the test topology     |")
    print("| 5 - Atack the network              |")
    print("| 0 - Close the Mininet              |")
    print("|------------------------------------|")

    opt = raw_input("\nChoice: ")

    return opt

net = None
opt = 1
setLogLevel('info')

print parser.parse_args().ip

while opt != "0":
    opt = menu()

    if opt == "0":
        print("Closing the Mininet")

    elif opt == "1":
        x = 1
        net = Mininet(topo = topology.topo_test(), build = False, autoSetMacs = True, controller = partial(RemoteController, ip = '127.0.0.1'))
	print("net: ", net)
        #net.addController('c0')     # To let the controller in the local mode
        net.start()                  # Init the network

    elif opt == "2":                 # Ping between  all devices
        net.pingAll()

    elif opt == "3":                 # Show all IP's
	print " Host    IP"
        for host in net.hosts:
            print "  " + str(host) + "  " + host.IP()

    elif opt == "4":
        net.stop()

    elif opt == "5":
       for i in range(1, 5000):
       	    print h3.cmd('ping -c1 %s' % h4.IP())

    raw_input("Press [Enter] to continue...")
