from flask import Flask, request, jsonify
import time
import requests

app = Flask(__name__)

# Global variables for state and logs
state = "INIT"
state_log = []
request_count = 0
start_time = time.time()

def log_state_change(previous_state, new_state):
    global state_log
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    state_log.append(f"{timestamp}: {previous_state} -> {new_state}")

@app.route('/', methods=['GET'])
def home():
    """Default route for testing."""
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


@app.route('/info', methods=['GET'])
def info():
    try:
        # Fetch information from service2
        response = requests.get('http://service2:8199/info')
        if response.status_code == 200:
            service2_data = response.json()
            return jsonify({"Service2": service2_data}), 200
        else:
            return f"Service2 returned status {response.status_code}", 503
    except requests.exceptions.RequestException as e:
        return str(e), 500

@app.route('/state', methods=['PUT'])
def set_state():
    global state
    new_state = request.data.decode('utf-8').strip()
    valid_states = ["INIT", "PAUSED", "RUNNING", "SHUTDOWN"]

    if new_state not in valid_states:
        return "Invalid state", 400

    if state != new_state:
        log_state_change(state, new_state)
        state = new_state

    return jsonify({"state": state})

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({"state": state})

@app.route('/request', methods=['GET'])
def handle_request():
    if state != "RUNNING":
        return "System not in RUNNING state", 403
    return "Request processed successfully"

@app.route('/run-log', methods=['GET'])
def get_run_log():
    return jsonify({"state_log": state_log})

@app.route('/monitor', methods=['GET'])
def monitor():
    """Endpoint for monitoring the service."""
    global request_count
    uptime = time.time() - start_time
    return jsonify({
        "uptime": f"{uptime:.2f} seconds",
        "total_requests": request_count,
        "current_state": state
    })

@app.before_request
def log_request():
    """Log each request and update the request count."""
    global request_count
    request_count += 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)
