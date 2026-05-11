import json
import ipaddress
import socket
from urllib.parse import urlparse
from urllib.request import urlopen
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
SAFE_SCHEMES = {"http", "https"}


def _is_public_target(hostname):
    try:
        addresses = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    resolved = set()
    for entry in addresses:
        resolved.add(entry[4][0])

    if not resolved:
        return False

    for address in resolved:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return False
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            return False
    return True


def _is_allowed_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in SAFE_SCHEMES or not parsed.hostname:
        return False
    return _is_public_target(parsed.hostname)

@app.route('/', methods=['GET'])
def health():
    return json.dumps({"STATUS":"HEALTHY"})

@app.route('/test-hook', methods=['POST'])
def ssrf():
    url = request.form.get('handler', '').strip()
    if not _is_allowed_url(url):
        return json.dumps({"error": "Target URL is not allowed"}), 400
    try:
        response_text = urlopen(url, timeout=5).read().decode("utf-8", "backslashreplace")
    except Exception:
        return json.dumps({"error": "Unable to fetch target URL"}), 502
    return json.dumps({"content":response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
