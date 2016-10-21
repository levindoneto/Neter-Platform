#!/usr/bin/python
# coding: UTF-8

import collections
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
'''#Define'''
SWITCH_INFO    = 0
MATCH_INFO     = 1
MATCH_PACK     = 0
DST_PACK       = 1
DST_INFO       = 2
ACTION_INFO    = 3
VISITED_INFO   = 4
IS_ORDERED     = 1
IS_NOT_ORDERED = 0

csvData = "../data/data.csv"

class NetQueue: # just an implementation of a queue
	def __init__(self):
		self.holder = []

	def enqueue(self,val):
		self.holder.append(val)

	def dequeue(self):
		val = None
		try:
			val = self.holder[0]
			if len(self.holder) == 1:
				self.holder = []
			else:
				self.holder = self.holder[1:]
		except:
			pass

		return val

	def IsEmpty(self):
		result = False
		if len(self.holder) == 0:
			result = True
		return result

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges

def find_isolated_nodes(graph):
    """ returns a list of isolated nodes. """
    isolated = []
    for node in graph:
        if not graph[node]:
            isolated += node
    return isolated

''' Convert a list of rules and others informations in a graph
    @:parameter : BV Lists: switches, match, destination, action
    @:return    : BV Graph '''
def make_graph(diffSwitches, switch_rule, match, destination, action, visited): # Type of all parameters -> List of BitVectors
    graph = {}                              # __INIT the graph network topology
    for switch in range(len(diffSwitches)): # Iterations = Number of rules in the network topology
        rulesInTheSwith = []                # Format: [[Switch0, Match0, Destination0, Action0],[Switch1, Match1, Destionation1, Action1],...] -> BitVector Elements
                                            # __init__ the list each switch

        for ruleVertice in range(len(destination[switch])):
            rulesInTheSwith.append([])      # Each list of that contains informations about one rule
            ''' Access the position ruleVertice of rulesInTheSwitch (Dynamic allocation) and
                add switch of the rule, getting a lists of information in this way:
                information->switch->ruleVertice
            '''
            rulesInTheSwith[ruleVertice].append(switch_rule[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(match[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(destination[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(action[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(visited[switch][ruleVertice])
        #print "PRIMEIRO DST COOL: ", rulesInTheSwith[0][0]
        graph.update({classBit.makeBitVector(switch+1):rulesInTheSwith}) # Update at graph with Sw : rule_list->rule_information->(match, dst, action)
    return graph

def BFS(graph,start,end,q):
	temp_path = [start]
	
	q.enqueue(temp_path)
	
	while q.IsEmpty() == False:
		tmp_path = q.dequeue()
		last_node = tmp_path[len(tmp_path)-1]
		print tmp_path
		if last_node == end:
			print "VALID_PATH : ",tmp_path
		for link_node in graph[last_node]:
			if link_node not in tmp_path:
				new_path = []
				new_path = tmp_path + [link_node]
				q.enqueue(new_path)

''' This method given a package, search this package in a network topology
	(graph of rules).
    @:parameter : BV package(list[match, dst]), BV graph
    @:return    : BV Graph '''
def graphSearch(package, network_topology, link_sw_host):
    Reachability = False   # False: Reachability isn't ok, True: Reachability is ok
    network_topology = collections.OrderedDict(sorted(network_topology.items()))
    print "This is the destination of the package: ", package[DST_PACK]
    node   = network_topology.values()
    switches   = network_topology.keys()
    # Switch tests
    '''
    i=0
    for n in switches:                  # Print the switches (ordered) at the topology
        print "Switch of the topology: ", switches[i]
        i+=1
    '''
    # Searching package->match at the list of rules of all switches
    for s in range(len(node)):
        #print "LOOK: ", s
        for r in range(len(node[s])):
            if (package[MATCH_PACK] == node[s][r][MATCH_INFO] and node[s][r][VISITED_INFO] != classBit.makeBitVector(1)): # package->match == node[s]->rule[r]->match_info
                #print "\n\nPackage was founded in ", r, "at the switch", s+1
                classBitList.route_action.append(node[s][r][ACTION_INFO])
                classBitList.route_switch.append(node[s][r][SWITCH_INFO])
                node[s][r][VISITED_INFO] = classBit.makeBitVector(1)         # node[s]->rule[r]->visited = 1
                sw_index_sought   = s
                #print ">>", s
                rule_index_sought = r
                #print ">>", r
                graph_Search(node, rule_index_sought, sw_index_sought, network_topology)

                if(package[DST_PACK] in link_sw_host[classBit.bvToInt(node[s][r][SWITCH_INFO])] and node[s][r][DST_INFO]==package[DST_PACK] and node[s][r][VISITED_INFO] == classBit.makeBitVector(1)):
                    Reachability = True
                else:
                    pass
    return Reachability                                                             # Package didn't arrives to its destination
''' Overloading of graphSearch method
	(graph of rules).
    @:parameter : BV package(list[match, dst]), BV graph
    @:return    : Bit Vector (stop can 0 or 1) '''
def graph_Search(node, sw_sought, rule_sought, network_topology):
    stop = classBit.makeBitVector(0)

    # Searching package->match at the list of rules of all switches
    for s in range(len(node)):
        for r in range(len(node[s])):
            if (node[s][rule_sought][MATCH_INFO] == node[s][r][MATCH_INFO] and node[s][r][VISITED_INFO] != classBit.makeBitVector(1)):
                #print "Package was founded in ", r, "at the switch", s+1 # Switch starts at one
                node[s][r][VISITED_INFO] = classBit.makeBitVector(1)     # node[s]->rule[r]->visited = 1
                #print "I got here!"
                sought = node[s][r][MATCH_INFO]                          # sought = node[s]->rule[r]->match

                rule_action = node[s][r][ACTION_INFO]
                rule_match = node[s][r][MATCH_INFO]

                #graph_Search(switches[s][r][match_info], network_topology, switches[s][r][action_info])
    return stop