#!/usr/bin/env python

from mininet.topo import Topo

class topo_test(Topo):

    def __init__(self):

        Topo.__init__(self)

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
	h3 = self.addHost('h3')      # Host malicioso
	h4 = self.addHost('h4')
	h5 = self.addHost('h5')       
	s1 = self.addSwitch('s1')    # Switch central
	s2 = self.addSwitch('s2')        
	s3 = self.addSwitch('s3')	
	
	# Interligando os hosts e o switch com topologia estrela
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
	self.addLink(h3, s2)
        self.addLink(h4, s3)
        self.addLink(h5, s3)
