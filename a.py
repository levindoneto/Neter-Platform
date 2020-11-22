N_HOSTS_HERE = 4
N_SWITCHES_HERE = 4
###############################################
from mininet.topo import Topo
import time
import argparse
from functools import partial # for using the RemoteController
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
import logging

logger = logging.getLogger("topology")

logging.basicConfig(level = logging.DEBUG)

''' Class to create the topology object based on the parameters from the POST request.
    @:parameter: mininet.topo: Topo
    @:parameter: list: hosts
    @:parameter: list: switches
    @:parameter: list of objects: links
{
    hosts: [<INTEGER>],
    swiches: [<INTEGER>],
    auto_set_macs: <BOOLEAN>,
    ip: <STRING>,
    links: <OBJECT> // e.g.: h1: [h1, h2], s1: [h1, h2]
}
'''
class topologyMininet(Topo):
	def __init__(self, hosts, switches, links):
		Topo.__init__(self)
		listHosts = []
		listSwitches = []
		logger.info("Init Mininet topology")
 		#try:
		for i in range(len(hosts)):
			time.sleep(1)
			listHosts.append(self.addHost('h' + str(hosts[i])))
		for i in range(len(switches)):
			time.sleep(1)
			listSwitches.append(self.addSwitch('s' + str(switches[i])))
		logger.info("Added Hosts: %s" % str(listHosts))
		logger.info("Added Switches: %s" % str(listSwitches))
		#except:
		#	logger.error("On creating devices for the topology")
		# Link the hosts and the switches
		for i in links:
			for j in links[i]:
				try:
					time.sleep(1)
					self.addLink(i, j)
					logger.info("Added link of " + i + " to " + j)
				except:
					logger.error("On adding link of " + i + " to " + j)

DEFAULT_IP = "127.0.0.1"
logger = logging.getLogger("mininet")
logging.basicConfig(level = logging.INFO)
parser = argparse.ArgumentParser(description = "Mininet Script")
parser.add_argument("--ip", action = "store", dest = "ip", default = DEFAULT_IP, required = False, help = "Controller IP")
net = None

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

def startNetwork(auto_set_macs, hosts, ip, links, switches):
    global net
    net = Mininet(topo = topologyMininet(hosts, switches, links), build = False, autoSetMacs = auto_set_macs, controller = partial(RemoteController, ip = ip))
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

n_hosts = N_HOSTS_HERE
n_switches = N_SWITCHES_HERE
hosts = range(1, n_hosts+1)
switches = range(1, n_switches+1)
auto_set_macs = False
ip =  "127.0.0.1"
links = dict()
for s in switches:
    links_s = ['s'+str(i) for i in switches if i != s] + ['h'+str(i) for i in hosts]
    links.update({"s"+str(s): links_s})
for h in hosts:
    links_h = ['s'+str(i) for i in switches] + ['h'+str(i) for i in hosts if i != h]
    links.update({"h"+str(h): links_h})

startNetwork(auto_set_macs, hosts, ip, links, switches)

while True:
    time.sleep(10)
    logger.info("-> Up")