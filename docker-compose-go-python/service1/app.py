import requests
from flask import Flask, jsonify
import subprocess
import logging

app = Flask(__name__)

def execute_command(command):
    """Helper function to run system commands and return output."""
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed: {e}")
        return None

def get_system_info():
    """Gather system information."""
    return {
        "IP address": execute_command("hostname -I"),
        "Running processes": execute_command("ps -ax"),
        "Available disk space": execute_command("df -h /"),
        "Uptime": execute_command("uptime -p")
    }

@app.route('/', methods=['GET'])
def index():
    service1_info = get_system_info()
    service2_info = None
    try:
        response = requests.get('http://service2:8080', timeout=5)
        response.raise_for_status()
        service2_info = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get data from Service2: {e}")
        service2_info = {"error": "Service2 unavailable"}
    return jsonify({
        "Service1": service1_info,
        "Service2": service2_info
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8199)
