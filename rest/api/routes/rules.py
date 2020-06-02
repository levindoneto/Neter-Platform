from flask import Blueprint, request, jsonify
from services import rules_service as Rules

rules_route = Blueprint('rules_route', __name__)

@rules_route.route("/rules/verifyRulesFlowtable", methods=["GET"])
def verifyRulesFlowtable():
    return jsonify(Rules.verifyFlowtable())

@rules_route.route("/rules/verifyRulesFirewall", methods=["GET"])
def verifyRulesFirewall():
    return jsonify(Rules.verifyFirewall())