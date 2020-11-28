from flask import Blueprint, request, jsonify
from services import rules_service as Rules
from flask_cors import CORS, cross_origin

rules_route = Blueprint('rules_route', __name__)
CORS(rules_route)

@rules_route.route("/rules/flowtable/conflicts", methods=["GET"])
def getConflictsFlowtable():
    verifiedFlowtable = Rules.verifyFlowtable('127.0.0.1', '8010')
    verificationId = verifiedFlowtable[0]
    time_elapsed = verifiedFlowtable[1]
    n_flows = verifiedFlowtable[2]
    memory_kilobytes = verifiedFlowtable[3]

    return jsonify(Rules.getConflictsFlowtable(verificationId, time_elapsed, n_flows, memory_kilobytes))

@rules_route.route("/rules/flowtable/redundancies", methods=["GET"])
def getRedundanciesFlowtable():
    verifiedFlowtable = Rules.verifyFlowtable('127.0.0.1', '8010')
    verificationId = verifiedFlowtable[0]
    time_elapsed = verifiedFlowtable[1]
    n_flows = verifiedFlowtable[2]
    memory_kilobytes = verifiedFlowtable[3]

    return jsonify(Rules.getRedundanciesFlowtable(verificationId, time_elapsed, n_flows, memory_kilobytes))

@rules_route.route("/rules/flowtable", methods=["GET"])
def getFlowtable():
    verificationId = Rules.verifyFlowtable('127.0.0.1', '8010')[0]
    print("verificationId: ", verificationId)
    return jsonify(Rules.getFlowtable(verificationId))