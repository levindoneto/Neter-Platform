#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from src.main.bitUtils import bfsGraphs as ClassGraph
from BitVector import BitVector
import time
'''Global Variables'''
switch_info  = 0
match_info   = 1
dst_info     = 2
action_info  = 3
visited_info = 4

csvData = "../data/arquivoDados.csv"

start = time.time()                                                         # init time

ALLOW = classBit.makeBitVector(1)
DENY = classBit.makeBitVector(0)

swinc = 0                                                                   # Switch counter (for CSV file)
# Parsing CSV (Rules)
auxMatchKey = BitVector(size=0)                                             # __init__ BitVect
rule_index = 0
with open(csvData, "rb") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    for row in spamreader:                                                  # Line by line of CSV file
        info_index = 0                                                      # Index of rule
        classBitList.ruleList.append([])
        for ind in range(len(row)):                                         # Column by column of CSV file
            row[info_index] = classBit.stringToIntFormated(row[info_index]) # String -> Int
            row[info_index] = classBit.makeBitVector(row[info_index])       # Int -> BitVector
            classBitList.ruleList[rule_index].append(row[info_index])       # Add in the list the BitVectors
            info_index += 1
        rule_index += 1

swinc = 0
classBitList.theSwitchList.append(classBit.makeBitVector(swinc))
classBitList.dstList.append([])
classBitList.switchList.append([])
classBitList.actionList.append([])
#predicate=0

for rule_index in range(len(classBitList.ruleList)):
    if (len(classBitList.ruleList[rule_index]) == 0): # Row == None
        swinc+=1
        classBitList.dstList.append([])
        classBitList.switchList.append([])
        classBitList.actionList.append([])
        classBitList.switchMatch.append([])
        classBitList.theSwitchList.append(classBit.makeBitVector(swinc))             # Add a different switch in the network topology

    else:
        classBitList.switchList[swinc].append(classBit.makeBitVector(swinc))         # Switch [0]
        classBitList.dstList[swinc].append(classBitList.ruleList[rule_index][6])     # Destination [2]
        classBitList.actionList[swinc].append(classBitList.ruleList[rule_index][-1]) # Action [3]
        classBitList.switchMatch.append(classBit.makeBitVector(swinc))               # Switch <-> Match
''' Making the match list'''
indexBV_rule = 0
# Catch match's informations and put this in a specific list for it
for rule_id in classBitList.ruleList:                  # Rule by rule
    auxPredicate = BitVector(size=0)
    for info_id in rule_id[0:-1]:                      # [information a information of a rule, without action]
        auxPredicate += info_id                        # Forming a BitVector mask predicate
    # Here the ruleList can be modified, because it has been used
    classBitList.ruleList[indexBV_rule] = auxPredicate # list_rules(list of informations) <- list_rules(BV predicate mask)
    indexBV_rule += 1

''' Link between switches and matches '''
switchM = 0                                            # Switch of a match
classBitList.matchList.append([])
for StoM in range(len(classBitList.switchMatch)):
    if len(classBitList.switchMatch[StoM]) == 0:       # Change switch
        classBitList.matchList.append([])
        switchM += 1
    else:
        classBitList.matchList[switchM].append(classBitList.ruleList[StoM])

'''*************************************************************************************************
****  General execution of Reachability Verification with a network topology in a graph format  ****
*************************************************************************************************'''

# Making the BV network graph
''' graph_t is the topology test in a graph format'''

''' It's working
// @DEBUG Topology Network Graph
#print type(graph_topology)
aux_listK = graph_topology.keys()
print aux_listK[0]
aux_listV = graph_topology.values()
print aux_listV[0][0][0][0]
'''

# Creating a package list
''' The list of parameters of parameters is converted in a list
*   of BitVector informations, that are Match and Destination
*   of the package.
'''
package_t = [1,2,98,1,9007199254740992,3,4,800,3]
package_t = classBit.makeTest(package_t)

''' Package enters in the topology network graph, the search is
*   made by a iterative bitwise comparison, that is made by a
*   XNOR gate between the package->match and the matches of
*   node->rule_list->match (This node is a graph vertice that
*   contains informations about a rule, these informations are
*   match, destination, switch and action of the rule)
'''

print "There are ", len(classBitList.theSwitchList), "in the network topology\n"

graph_topology = ClassGraph.make_graph(classBitList.theSwitchList, classBitList.switchList, classBitList.matchList, classBitList.dstList, classBitList.actionList)

ClassGraph.graphSearch(package_t, graph_topology)
topology_link = "../../../../topology_link.csv"

classBit.getLink(topology_link)


''' The graph vertices has informations about the rules
*   Each vertice of the network graph contains [i][j][k][l]
*   [i]: It varies with the switch
*   [j]: It varies with the rule
*   [0]: Switch  [1]: Match  [2]: Destination  [3]:Action [4]:Visited
'''

#print 2 ^ 3  # 10 xor 11 => 01    #xor

end = time.time()
print (end - start), "seconds"