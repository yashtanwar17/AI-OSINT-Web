import requests

COMMON_PATHS = [
    "assets", "uploads", "images", "img", "files", "downloads", "backup", "backups", "logs",
    "private", "media", "tmp", "temp", "storage", "public", "scripts", "js", "css", "static",
    "includes", "old", "data", "db", "conf", "config", "admin", "archive", "archives", "documents"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_directory_listing_enabled(html: str) -> bool:
    html = html.lower()
    return any(tag in html for tag in [
        "index of /", "<title>index of", "parent directory", "name", "last modified", "size"
    ])

def scan_directory_listing(base_url):
    if not base_url.startswith("http"):
        base_url = "http://" + base_url
    if not base_url.endswith("/"):
        base_url += "/"

    print(f"\n[~] Scanning for directory listings at {base_url}\n")
    for path in COMMON_PATHS:
        url = f"{base_url}{path}/"
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
            if response.status_code == 200 and is_directory_listing_enabled(response.text):
                print(f"[!] Directory listing ENABLED: {url}")
            elif response.status_code == 403:
                print(f"[-] Forbidden (403): {url}")
            elif response.status_code == 404:
                continue  # Skip not found
            else:
                print(f"[~] Checked (code {response.status_code}): {url}")
        except requests.RequestException:
            print(f"[x] Error accessing: {url}")

