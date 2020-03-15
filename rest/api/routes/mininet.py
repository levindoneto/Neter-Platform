from flask import Blueprint, request, jsonify
# from services import mininet as Mininet

mininet_route = Blueprint('mininet_route', __name__)

@mininet_route.route('/mininet/start', methods=['POST'])
def topology():
    content = request.json
    auto_set_macs = content['autoSetMacs']
    hosts = content['hosts']
    ip = content['ip']
    links = content['links']
    switches = content['switches']
    Mininet.startNetwork(auto_set_macs, hosts, ip, links, switches)
    return jsonify({"status": "Topology started on IP " + ip})

@mininet_route.route('/mininet/ping', methods=['POST'])
def ping():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/ips', methods=['GET'])
def get_ips():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/stop', methods=['POST'])
def stop():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/attack', methods=['POST'])
def attack():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/close', methods=['POST'])
def close():
    return "NOT IMPLEMENTED"
