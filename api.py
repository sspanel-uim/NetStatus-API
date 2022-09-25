import socket
from flask import Flask, request, jsonify
import gevent.pywsgi

app = Flask(__name__)
app.config['PORT'] = 8080
app.config['TIMEOUT'] = 1  # In seconds
app.config['VERSION'] = 1

@app.route('/tcping', methods=['GET'])
def tcping():
    request_parameters = request.args
    ip = request_parameters.get('ip')
    port = request_parameters.get('port')
    if ip is None:
        return jsonify({"status": "error", "message": "Missing ip parameter"})
    if port is None:
        return jsonify({"status": "error", "message": "Missing port parameter"})
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.settimeout(app.config['TIMEOUT'])
    result = socks.connect_ex((ip, int(port)))
    socks.close()
    if result == 0:
        return jsonify({"status": "true"})
    else:
        return jsonify({"status": "false"})

@app.errorhandler(404)
def page_not_found(e):
    return "<p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', app.config['PORT']), app)
    app_server.serve_forever()
