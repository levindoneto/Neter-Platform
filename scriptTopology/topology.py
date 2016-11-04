#!/usr/bin/env python

from mininet.topo import Topo

class topo_test(Topo):

	def __init__(self):

		Topo.__init__(self)

		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')
		h5 = self.addHost('h5')  
		h5 = self.addHost('h6') 
		h5 = self.addHost('h7') 
		h5 = self.addHost('h8')      
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')        
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')	
	
		# Link the hosts and the swithces
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(h3, s2)
        self.addLink(h4, s3)
        self.addLink(h5, s3)
        self.addLink(s3, s4)
        self.addLink(s4, h6)
        self.addLink(s4, h7)
        self.addLink(s4, s5)
        self.addLink(s5, h8)