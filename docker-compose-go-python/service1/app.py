import requests
import json
from flask import Flask, jsonify

app = Flask(__name__)

def get_system_info():
    # Get info from Service2
    try:
        response = requests.get('http://service2:8199/info')
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/info', methods=['GET'])
def info():
    # Collect data from Service1 (this container) and Service2
    system_info = {
        "Service1": {
            "ip_address": requests.get('https://api.ipify.org').text,
            "processes": open('/proc/self/status').read(),
            "disk_space": open('/proc/mounts').read(),
            "uptime": open('/proc/uptime').read().split()[0]
        },
        "Service2": get_system_info()
    }
    return jsonify(system_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8199)
