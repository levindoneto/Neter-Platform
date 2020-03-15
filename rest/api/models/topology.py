#!/usr/bin/env python

from mininet.topo import Topo

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
class topologyMininet(Topo, hosts, switches, links):
	def __init__(self, hosts, switches, links):
		Topo.__init__(self)
		listHosts = []
		listSwitches = []
		for i in range(len(hosts)):
			listHosts[i].append(self.addHost('h' + str(hosts[i])))
		for i in range(len(hosts)):
			listSwitches.append(self.addSwitch('s' + str(swiches[i])))
		# Link the hosts and the swithces
		for i in links:
			for j in links[i]:
				self.addLink(i, j)