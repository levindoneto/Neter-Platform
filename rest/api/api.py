import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/topology', methods=['POST'])
def topology():
    return True

@app.route('/ping', methods=['POST'])
def ping():
    return True

@app.route('/ips', methods=['GET'])
def get_ips():
    return True

@app.route('/stop', methods=['POST'])
def stop():
    return True

@app.route('/attack', methods=['POST'])
def attack():
    return True

@app.route('/close', methods=['POST'])
def close():
    return True

app.run()
