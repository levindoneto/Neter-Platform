from flask import Flask, jsonify
from routes.conflicts import conflicts_route
from routes.mininet import mininet_route
from routes.reachability import reachability_route
from routes.redundancies import redundancies_route


app = Flask(__name__)

app.register_blueprint(conflicts_route)
app.register_blueprint(mininet_route)
app.register_blueprint(reachability_route)
app.register_blueprint(redundancies_route)

@app.route("/")
def docs():
    return "Placidus SDN Manager"

if __name__ == "__main__":
    app.run()