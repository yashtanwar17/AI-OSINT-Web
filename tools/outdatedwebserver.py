import requests
import re

# June 2025
latest_versions = {
    "Apache": "2.4.59",
    "nginx": "1.26.0",
    "Microsoft-IIS": "10.0",
    "LiteSpeed": "6.1",
    "Gunicorn": "21.2.0",
    "OpenResty": "1.25.3.1",
    "Caddy": "2.8.4",
    "Tomcat": "10.1.20",
    "Node.js": "20.13.1"
}

def parse_version(header_value):
    """Extracts server type and version number."""
    for server_name in latest_versions:
        if server_name.lower() in header_value.lower():
            match = re.search(rf"{server_name}[^\d]*(\d+(\.\d+)+)", header_value, re.IGNORECASE)
            if match:
                return server_name, match.group(1)
            else:
                return server_name, None
    return None, None

def compare_versions(current, latest):
    def normalize(v):
        return tuple(map(int, (v.split("."))))
    try:
        return normalize(current) >= normalize(latest)
    except:
        return False

def check_server_version(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        server_header = response.headers.get("Server", "")
        if not server_header:
            print("No Server header found.")
            return

        print(f"[+] Server header: {server_header}")
        server_type, version = parse_version(server_header)

        if server_type:
            latest = latest_versions[server_type]
            if version:
                if compare_versions(version, latest):
                    print(f"[✅] {server_type} is up-to-date ({version})")
                else:
                    print(f"[⚠️] {server_type} is outdated! ({version} < {latest})")
            else:
                print(f"[❓] Apache detected, but version hidden.")
        else:
            print("[❓] Server type not recognized.")

    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")

