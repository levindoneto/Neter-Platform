from flask import Flask, jsonify
from flask_cors import CORS
from routes.rules import rules_route
from routes.mininet import mininet_route
from routes.reachability import reachability_route


app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(rules_route)
app.register_blueprint(mininet_route)
app.register_blueprint(reachability_route)

@app.route("/")
def docs():
    return "Placidus SDN Manager"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8060)
