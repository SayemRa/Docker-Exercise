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
    print(f"LOG: {STATE_LOG}")  # Debugging

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

API_KEY = "my_secure_key"

def validate_api_key():
    """
    Validates the API Key in the request headers.
    """
    api_key = request.headers.get("X-API-KEY")
    return api_key == API_KEY

@app.route('/state', methods=['PUT'])
def set_state():
    """
    Set the state of the system, requiring authentication.
    """
    global STATE
    if not validate_api_key():
        return jsonify({"error": "Unauthorized"}), 403

    new_state = request.get_data(as_text=True).strip()
    valid_states = ["INIT", "PAUSED", "RUNNING", "SHUTDOWN"]

    if new_state not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

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
    global REQUEST_COUNT, START_TIME
    uptime_seconds = round(time.time() - START_TIME, 2)

    return jsonify({
        "uptime": uptime_seconds,
        "total_requests": REQUEST_COUNT,  
        "current_state": STATE
    }), 200


# app.py (Service1)
@app.route('/info', methods=['GET'])
def get_service2_info():
    try:
        response = requests.get("http://service2:8199/info")  
        if response.status_code == 200:
            service2_data = response.json()
            return jsonify({"Service2": service2_data}), 200
        return jsonify({"error": "Service2 unavailable"}), 503
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch Service2 data"}), 500
    


@app.route('/run-log', methods=['GET'])
def get_run_log():
    """
    Returns the logged state transitions, even in SHUTDOWN state.
    """
    return jsonify({"logs": STATE_LOG}), 200

@app.before_request
def check_shutdown():
    """
    Prevent all requests when in SHUTDOWN state, except essential ones.
    """
    global STATE
    allowed_paths = ["/state", "/monitor", "/run-log"]
    if STATE == "SHUTDOWN" and request.path not in allowed_paths:
        return jsonify({"error": "Service unavailable"}), 503

@app.before_request
def log_request():
    """
    Log each request and update the request count.
    """
    global REQUEST_COUNT
    REQUEST_COUNT += 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)
