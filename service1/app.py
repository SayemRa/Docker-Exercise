"""
Main module for Service1
"""
import time
from flask import Flask, request, jsonify
import requests

# Global variables
STATE = "INIT"
STATE_LOG = []
REQUEST_COUNT = 0
START_TIME = time.time()

app = Flask(__name__)

def log_state_change(previous_state, new_state):
    """
    Logs state transitions with a timestamp.
    """
    global STATE_LOG
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    STATE_LOG.append(f"{timestamp}: {previous_state} -> {new_state}")


@app.route('/', methods=['GET'])
def home():
    """
    Default route for testing.
    """
    return jsonify({
        "message": "Welcome to Service1! Available endpoints:",
        "endpoints": {
            "/state": "Manage or retrieve the system state",
            "/request": "Simulate a request",
            "/run-log": "View state transition logs",
            "/monitor": "View system monitoring information",
            "/info": "Retrieve information from Service2"
        }
    }), 200


@app.route('/state', methods=['PUT'])
def set_state():
    """
    Set the state of the system.
    """
    global STATE
    new_state = request.get_data(as_text=True).strip()
    valid_states = ["INIT", "PAUSED", "RUNNING", "SHUTDOWN"]

    if new_state not in valid_states:
        return "Invalid state", 400

    if STATE != new_state:
        log_state_change(STATE, new_state)
        STATE = new_state

    return jsonify({"state": STATE}), 200


@app.route('/state', methods=['GET'])
def get_state():
    """
    Get the current state of the system.
    """
    return jsonify({"state": STATE}), 200


@app.route('/monitor', methods=['GET'])
def monitor():
    """
    Monitor system metrics.
    """
    uptime = time.time() - START_TIME
    return jsonify({
        "uptime": f"{uptime:.2f} seconds",
        "total_requests": REQUEST_COUNT,
        "current_state": STATE
    }), 200


@app.before_request
def log_request():
    """
    Log each request and update the request count.
    """
    global REQUEST_COUNT
    REQUEST_COUNT += 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)
