import os
import json
import ipaddress
import logging
import socket
from urllib.parse import parse_qs, unquote, urlparse
from urllib.error import URLError
from urllib.request import urlopen

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

def handler(event, context):
    body = event.get("body") or ""
    params = parse_qs(unquote(body), keep_blank_values=True)
    url = params.get("handler", [""])[0].strip()
    target_url = _get_allowed_target(url)
    print(f"URL: {url}")

    if target_url is None or not _is_allowed_url(url):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Target URL is not allowed"}),
            "headers": {
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Origin": os.environ["CORS"],
                "Content-Type": "application/json"
            }
        }

    try:
        response_text = urlopen(target_url, timeout=5).read().decode("utf-8", "backslashreplace")
    except (TimeoutError, URLError, ValueError) as exc:
        LOGGER.warning("Target fetch failed: %s", exc)
        return {
            "statusCode": 502,
            "body": json.dumps({"error": "Unable to fetch target URL"}),
            "headers": {
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Origin": os.environ["CORS"],
                "Content-Type": "application/json"
            }
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "content": response_text
            }
        ),
        "headers": {
            "Access-Control-Allow-Methods":
                "OPTIONS,POST",
            "Access-Control-Allow-Origin": os.environ["CORS"],
            "Content-Type": "application/json"
        }
    }
