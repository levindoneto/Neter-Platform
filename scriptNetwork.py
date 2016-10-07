#!/usr/bin/env python

import time
import topology
import argparse
from functools import partial #to can use the RemoteController

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
from os import system

parser = argparse.ArgumentParser(description = "Mininet Script")
parser.add_argument("--ip", action = "store", dest = "ip", default = "localhost", required = False, help = "Controller IP")

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
	#143.54.12.10
        net = Mininet(topo = topology.topo_test(), build = False, autoSetMacs = True, controller = partial(RemoteController, ip = '143.54.12.10', port=6653))

        #net.addController('c0')     # For to let the controller in the local mode
        net.start()                  # Init the network

	''' Os ip's podem ser gerados automaticamente ou setados a partir daqui '''
'''
        h1 = net.getNodeByName("h1") # setando ip no h1
	h1.setIP("10.0.0.1", 8)      # (IP, Mascara)
	
	h2 = net.getNodeByName("h2") # setando ip no h2
        h2.setIP("10.0.0.2", 8)      # (IP, Mascara)	
	
	h4 = net.getNodeByName("h4") # Setando ip no h4
        h4.setIP("10.0.0.4", 8)      # (IP, Mascara)	
	
	''' Setando IP maligno para teste '''
	h3 = net.getNodeByName("h3") # Setando ip no h3
        h3.setIP("10.0.0.3", 8)

	h5 = net.getNodeByName("h5") # Setando ip no h5
        h5.setIP("10.0.0.5", 8)
'''
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
