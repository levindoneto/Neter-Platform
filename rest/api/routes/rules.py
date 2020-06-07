from flask import Blueprint, request, jsonify
from services import rules_service as Rules

rules_route = Blueprint('rules_route', __name__)

@rules_route.route("/rules/flowtable/conflicts", methods=["GET"])
def getConflictsFlowtable():
    verificationId = Rules.verifyFlowtable('127.0.0.1', '8010')
    return jsonify(Rules.getConflictsFlowtable(verificationId))

@rules_route.route("/rules/flowtable/redundancies", methods=["GET"])
def getRedundanciesFlowtable():
    verificationId = Rules.verifyFlowtable('127.0.0.1', '8010')
    return jsonify(Rules.getRedundanciesFlowtable(verificationId))

@rules_route.route("/rules/flowtable", methods=["GET"])
def getFlowtable():
    verificationId = Rules.verifyFlowtable('127.0.0.1', '8010')
    return jsonify(Rules.getFlowtable(verificationId))