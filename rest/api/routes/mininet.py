from flask import Blueprint, request, jsonify
from services import mininet_service as Mininet

mininet_route = Blueprint('mininet_route', __name__)

@mininet_route.route('/mininet/start', methods=['POST'])
def start():
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
    Mininet.pingAll()
    return jsonify({"status": "Ping all completed"})

@mininet_route.route('/mininet/ips', methods=['GET'])
def get_ips():
    ips = Mininet.getHosts()
    return jsonify({"ips": ips})

@mininet_route.route('/mininet/stop', methods=['POST'])
def stop():
    Mininet.stopNetwork()
    return jsonify({"status": "Network stopped"})

@mininet_route.route('/mininet/attack', methods=['POST'])
def attack():
    Mininet.attackNetwork()
    return jsonify({"status": "Network attacked"})

@mininet_route.route('/mininet/close', methods=['POST'])
def close():
    Mininet.closeNetwork()
    return jsonify({"status": "Mininet closed"})
