#!/usr/bin/env python

from mininet.topo import Topo
import logging
import time

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
