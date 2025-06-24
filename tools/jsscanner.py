import requests
from bs4 import BeautifulSoup
import os
import re
import tempfile
import subprocess

def fetch_cdn_js_urls(url):
    print(f"[*] Fetching CDN scripts from {url} ...")
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"[!] Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    script_tags = soup.find_all("script", src=True)

    cdn_scripts = []
    for tag in script_tags:
        src = tag["src"]
        if src.startswith("http") and ("cdn" in src or "cloudflare" in src):
            cdn_scripts.append(src)

    if cdn_scripts:
        print(f"[+] Found {len(cdn_scripts)} CDN JS scripts.")
    else:
        print("[!] No CDN JS scripts found.")
    return cdn_scripts

def download_js_files(script_urls, temp_dir):
    local_files = []
    for url in script_urls:
        try:
            response = requests.get(url, timeout=10)
            filename = re.sub(r'[^\w\-_.]', '_', url.split("/")[-1].split("?")[0] or "index.js")
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
                f.write(response.text)
            local_files.append(filepath)
            print(f"[+] Downloaded {url}")
        except Exception as e:
            print(f"[!] Failed to download {url}: {e}")
    return local_files

def scan_with_retire(temp_dir):
    print("[*] Scanning downloaded files with Retire.js...")
    try:
        retire_js_path = os.path.abspath(
            "retire.js-5.2.7/node/lib/retire.js"
        )
        result = subprocess.run(
            ["node", retire_js_path, "--path", temp_dir],
            capture_output=True, text=True, check=False
        )
        output = result.stdout.strip()
        if output:
            print(output)
        else:
            print("✅ No known vulnerabilities detected.")
    except FileNotFoundError:
        print("[!] Node.js not found. Please make sure it's installed and in PATH.")
    except subprocess.CalledProcessError as e:
        print("[!] Retire.js reported an error:\n", e.stdout, e.stderr)


def main():
    
    target_url = "https://getbootstrap.com"
    cdn_js_urls = fetch_cdn_js_urls(target_url)

    if not cdn_js_urls:
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        download_js_files(cdn_js_urls, temp_dir)
        scan_with_retire(temp_dir)

if __name__ == "__main__":
    main()
