from flask import Blueprint, request, jsonify
from services import rules_service as Rules

rules_route = Blueprint('rules_route', __name__)

@rules_route.route("/rules/flowtable/conflicts", methods=["GET"])
def getConflictsFlowtable():
    verifiedFlowtable = Rules.verifyFlowtable('127.0.0.1', '8010')
    verificationId = verifiedFlowtable[0]
    time_elapsed = verifiedFlowtable[1]
    n_flows = verifiedFlowtable[2]
    return jsonify(Rules.getConflictsFlowtable(verificationId, time_elapsed, n_flows))

@rules_route.route("/rules/flowtable/redundancies", methods=["GET"])
def getRedundanciesFlowtable():
    verifiedFlowtable = Rules.verifyFlowtable('127.0.0.1', '8010')
    verificationId = verifiedFlowtable[0]
    time_elapsed = verifiedFlowtable[1]
    n_flows = verifiedFlowtable[2]
    return jsonify(Rules.getRedundanciesFlowtable(verificationId, time_elapsed, n_flows))

@rules_route.route("/rules/flowtable", methods=["GET"])
def getFlowtable():
    verificationId = Rules.verifyFlowtable('127.0.0.1', '8010')
    return jsonify(Rules.getFlowtable(verificationId))