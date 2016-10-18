#!/usr/bin/python
# coding: UTF-8
import csv
import collections
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
'''Global Variables'''
switch_info    = 0
match_info     = 1
match_pack     = 0
dst_pack       = 1
dst_info       = 2
action_info    = 3
visited_info   = 4
is_ordered     = 1
is_not_ordered = 0

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
def graphSearch(package, network_topology):

    network_topology = collections.OrderedDict(sorted(network_topology.items()))

    print type(network_topology)

    switches   = network_rtopology.values()  # Can be done like this:: print "KEY DO DICT: ", network_topology[n]
    keys   = network_topology.keys()

    # Switch test keys
    print "Swiches in the GRAPH_SEARCH:"
    i=0

    for n in keys:
        print "KEY DO DICT: ", keys[i]
        i+=1


    ''' If it was sought
        switches[s]->rule[r]->visited = 1
        graph_Search(switches, topology)
    '''
    '''
    graph_Search(switches, topology) {
        for sw:
            for rule:
                if (switches[sw_index_sought]->rule[rule_index_sought]->match == switches[s][r][match_info] and switches[s][r][visited_info] != 1):
    }
    '''


    sought = BitVector(size=0) # Init of a BitVector with size 0
    # Searching package->match at the list of rules of all switches
    for s in range(len(switches)):
        for r in range(len(switches[s])):
            if (package[0] == switches[s][r][match_info]):
                print "\n\nPackage was founded in ", r, "at the switch", s+1
                switches[4][20][visited_info] = 1                          # node[s]->rule[r]->visited = 1
                sought = switches[s][r][match_info]                        # sought = node[s]->rule[r]->match

                print "DESTINO DA REGRA: ", switches[s][r][dst_info]
                print "DESTINO DO PACOTE:", package[1]
                print "ACAO DA REGRA", switches[s][r][action_info]

                #rule_match = switches[s][r][match_info]
                #rule_action = switches[s][r][action_info]
                sw_index_sought   = s
                rule_index_sought = r
                graph_Search(switches, rule_index_sought, sw_index_sought, network_topology)

                print "Visited information: ", switches[s][r][visited_info]

''' Overloading of graphSearch method
	(graph of rules).
    @:parameter : BV package(list[match, dst]), BV graph
    @:return    : Bit Vector (stop can 0 or 1) '''
def graph_Search(switches, sw, rule, network_topology):
    stop = classBit.makeBitVector(0)

    sought = BitVector(size=0) # Init of a BitVector with size 0
    # Searching package->match at the list of rules of all switches
    for s in range(len(switches)):
        for r in range(len(switches[s])):
            if (rule_match == switches[s][r][match_info]):
                print "Package was founded in ", r, "at the switch", s+1      # Switch starts at one
                switches[s][r][visited_info] = 1                            # node[s]->rule[r]->visited = 1
                sought = switches[s][r][match_info]                         # sought = node[s]->rule[r]->match

                rule_action = switches[s][r][action_info]
                rule_match = switches[s][r][match_info]

                #graph_Search(switches[s][r][match_info], network_topology, switches[s][r][action_info])

    return stop