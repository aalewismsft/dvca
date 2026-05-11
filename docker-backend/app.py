import json
import ipaddress
import logging
import os
import socket
from urllib.parse import urlparse
from urllib.error import URLError
from urllib.request import urlopen
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
SAFE_SCHEMES = {"http", "https"}
ALLOWED_FETCH_HOSTS = {
    host.strip().lower()
    for host in os.getenv("ALLOWED_FETCH_HOSTS", "").split(",")
    if host.strip()
}
ALLOWED_FETCH_URLS = tuple(
    target.strip()
    for target in os.getenv("ALLOWED_FETCH_URLS", "").split(",")
    if target.strip()
)
LOGGER = logging.getLogger(__name__)


def _is_public_target(hostname):
    try:
        addresses = socket.getaddrinfo(hostname, None)
    except (socket.gaierror, OSError):
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


def _get_allowed_target(url):
    for candidate in ALLOWED_FETCH_URLS:
        if candidate == url:
            return candidate
    return None


def _is_allowed_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in SAFE_SCHEMES or not parsed.hostname:
        return False
    if parsed.hostname.lower() not in ALLOWED_FETCH_HOSTS:
        return False
    return _is_public_target(parsed.hostname)

@app.route('/', methods=['GET'])
def health():
    return json.dumps({"STATUS":"HEALTHY"})

@app.route('/test-hook', methods=['POST'])
def ssrf():
    url = request.form.get('handler', '').strip()
    target_url = _get_allowed_target(url)
    if target_url is None or not _is_allowed_url(url):
        return json.dumps({"error": "Target URL is not allowed"}), 400
    try:
        response_text = urlopen(target_url, timeout=5).read().decode("utf-8", "backslashreplace")
    except (TimeoutError, URLError, ValueError) as exc:
        LOGGER.warning("Target fetch failed: %s", exc)
        return json.dumps({"error": "Unable to fetch target URL"}), 502
    return json.dumps({"content":response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
