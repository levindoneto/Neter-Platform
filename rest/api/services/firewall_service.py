#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time
import firewall_rules from ../constants as FIREWALL_RULES
import flowtable_rules from ../constants as FLOWTABLE_RULES

logger = logging.getLogger("firewall_service")
logging.basicConfig(level = logging.INFO)

def areRulesAvailable(objRule):
    for i in objRule.keys():
        return False if (!(i in FIREWALL_RULES.RULES) or !(i in FLOWTABLE_RULES.RULES))
    return True

"""
Add rule to firewall
@param: rawRule
Format:
{
   "switch": <str>,
   <str:property>:<str:value>,
   ...
}
"""
def addRule(objRule, ip, port):
    if (len(objRule) < 1):
        logger.error("New rule is empty")
        return {"error": "New rule is empty"}
    elif !("switch" in objRule):
        logger.error("New rule has no addressed switch")
        return {"error": "New rule has no addressed switch"}
    elif(areRulesAvailable(objRule)):
        rules = json.dumps(objRule)
        command = "curl -s -d " + rules + " http://" + ip + ":" + port + "/wm/staticflowpusher/json"
        command_output = os.popen(command).read()
        status = json.loads(command_output)
        return {"status": status}

"""
Delete rule from firewall
"""
def deleteRule(ruleId, ip, port):
    command = "curl -X DELETE -d " + "'{" + '"ruleid"' +  ":" + ruleId + "}' http:// + " + ip + ":" + port + "/wm/firewall/rules/json"
    command_output = os.popen(command).read()
    status = json.loads(command_output)
    return {"status": status}