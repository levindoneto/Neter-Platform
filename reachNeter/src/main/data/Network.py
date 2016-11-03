#!/usr/bin/python
# coding: UTF-8
import json
import os


# LER ARQUIVO E PARSEAR PRO FORMATO CERTO
# FAZER MAKE FILE PRA LIMPAR OS ~

''' Given an IP and Port, this method makes the csv table file that
    represents the networks flows. The IP:Port default is: 143.54.12.10:8080,
    this is used if the user pass i,p as a parameter for this method.
    @:parameter: String IP, String Port
    @:return: CSV Flowtable file
'''
def tableGenerator(ip, port):
    this_ip = ip
    this_port = port

    if (this_ip=='i' and this_port=='p'):
        this_ip =  "143.54.12.10"
        this_port = "8080"

    command = "curl -s http://" + this_ip + ":" + this_port + "/wm/core/switch/all/flow/json"

    command_output = os.popen(command).read()
    topology = json.loads(command_output)

    # Create the json file with de flows in the network topology
    dataflow = open("../data/dataflow.json", "w")
    dataflow.write(str(topology))
    dataflow.close()