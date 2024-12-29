from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Global variables for state and logs
state = "INIT"
state_log = []

def log_state_change(previous_state, new_state):
    global state_log
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    state_log.append(f"{timestamp}: {previous_state} -> {new_state}")

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)
