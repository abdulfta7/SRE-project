import requests
import time
import socket
import ssl
import json
import os
from datetime import datetime
import dns.resolver

TARGET_URL = "https://mithal.space"
TARGET_DOMAIN = "mithal.space"
DATA_FILE = "/Users/mac/a1/mithal_monitor/data/metrics.json"

def check_ssl(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_remaining = (expiry_date - datetime.utcnow()).days
                return "Valid", days_remaining
    except Exception as e:
        return f"Error: {str(e)}", 0

def check_dns(domain):
    start = time.time()
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return round((time.time() - start) * 1000, 2)
    except Exception:
        return -1

def measure():
    results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "latency_ms": -1,
        "status_code": 0,
        "uptime": False,
        "ssl_status": "Unknown",
        "ssl_days": 0,
        "dns_time_ms": -1,
        "search_time_ms": -1
    }
    
    # DNS Check
    results["dns_time_ms"] = check_dns(TARGET_DOMAIN)
    
    # SSL Check
    ssl_status, ssl_days = check_ssl(TARGET_DOMAIN)
    results["ssl_status"] = ssl_status
    results["ssl_days"] = ssl_days
    
    # HTTP Check
    try:
        start = time.time()
        resp = requests.get(TARGET_URL, timeout=5)
        results["latency_ms"] = round((time.time() - start) * 1000, 2)
        results["status_code"] = resp.status_code
        results["uptime"] = resp.status_code < 400
    except Exception:
        pass

    # Mock Search Check (assuming a /search endpoint exists)
    try:
        start = time.time()
        requests.get(f"{TARGET_URL}/search?q=test", timeout=5)
        results["search_time_ms"] = round((time.time() - start) * 1000, 2)
    except Exception:
        pass

    return results

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    history = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            pass
    
    history.append(data)
    # Keep last 1440 checks (24 hours at 1/min)
    history = history[-1440:]
    
    with open(DATA_FILE, 'w') as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    while True:
        data = measure()
        save_data(data)
        time.sleep(60)
