# Placidus: A Platform of formal verification in software defined networks
__Author:__ Levindo Gabriel Taschetto Neto

The Placidus is a formal verification platform for Software Defined Networks (SDN), and it has two modules that check the following properties: Conflicts and Redundancies logical rules formed from a network topology, and Reachability in a network topology.

![Logo of Placidus](resources/Logo-Placidus.jpg)

## Reachability verifier 

### Data Structure
http://prntscr.com/cixbjh
![Graph Network](reachNeter/src/main/resources/graph_network.png)

### Algorithm Proposed for the Verification of Reachability with the Graph Approach
![Algorithm proposed for Reachability Graph Verification](reachNeter/src/main/resources/algorithm_reachability_graph.jpg)

### Network topology for the tests
![Network for tests](reachNeter/src/main/resources/topology_network.png)

### Steps of execution:
* The input package is converted to a vector of bits, using the method makeTest of class bitVectorUtils.

* Package enters in the topology network graph, the search is made by a iterative bitwise comparison, that is made by a XNOR gate between the package->match and the matches of node->rule_list->match (This node is a graph vertice that contains informations about a rule, these informations are match, destination, switch, action and visited of the node.

* The link between switches and hosts is made with the method getLink of de class bitVectorUtils. This method returns a list where the switches are used as a index and the values of each index are the hosts.

* The following lists is obtained by the reading of the CSV file that contains the rules of the software defined network:
```python
classBitList.switchList    # This list contains only information about switches according the network topology {switch : rule}
classBitList.switchMatch   # This list is used for to link match and switches of network topology
classBitList.dstList       # This list contains only information about destination of packages in the network
classBitList.actionList    # This list contains only information about actions of predicates with the same index of the match informations
classBitList.theSwitchList # List of switches in the network topology
```
This lists is used to put informations at the nodes of the network topology graph.


* The reachability property is tested by a graph search at the topology network. One more information was added to the nodes of the graph of topology network, the visited information. This information is one of the informations used as a stop condition of breadth-first search that is made to verify if the package come in its destination of correct way.
