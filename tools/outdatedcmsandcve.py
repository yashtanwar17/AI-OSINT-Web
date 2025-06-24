import subprocess
import re
import shutil,os
import requests

# JUNE 2025
latest_cms_versions = {
    "WordPress": "6.5.3",
    "Joomla": "5.0.3",
    "Drupal": "10.3.0",
    "Magento": "2.4.7",
    "PrestaShop": "8.1.5",
    "OpenCart": "4.0.2.3",
    "TYPO3": "12.4.11",
    "Ghost": "5.83.4"
}

WHATWEB_PATH = os.path.join(os.path.dirname(__file__), "WhatWeb-0.5.5", "whatweb")  

def run_whatweb(url):
    if not os.path.isfile(WHATWEB_PATH):
        print(f"[❌] WhatWeb script not found at {WHATWEB_PATH}")
        return []

    try:
        result = subprocess.check_output(["ruby", WHATWEB_PATH, "-v", url], stderr=subprocess.DEVNULL, text=True)
        return result.splitlines()
    except Exception as e:
        print(f"[ERROR] WhatWeb failed: {e}")
        return []


def extract_cms_versions(whatweb_output):
    found = {}
    for line in whatweb_output:
        for cms in latest_cms_versions:
            if cms.lower() in line.lower():
                match = re.search(rf"{cms}[^\d]*([\d\.]+)", line, re.IGNORECASE)
                version = match.group(1) if match else None
                if cms not in found:
                    found[cms] = version
    return list(found.items())

def compare_versions(current, latest):
    def normalize(v): return tuple(map(int, (v or "").split(".")))
    try:
        return normalize(current) >= normalize(latest)
    except:
        return False

def fetch_cves(product, version):
    # Use just the product name to avoid 404
    query = product.lower()
    url = f"https://cve.circl.lu/api/search/{query}"
    print(f"\n🛡️ CVE search for {product} v{version}...")
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        results = data.get("results", [])
        if not results:
            print("✅ No CVEs found.")
            return
        filtered = [cve for cve in results if version in str(cve)]
        if not filtered:
            print("✅ No relevant CVEs found for this version.")
            return
        for cve in filtered[:10]:
            cve_id = cve.get("id", "N/A")
            summary = cve.get("summary", "No summary")
            print(f"[‼️] {cve_id}: {summary[:100]}...")
    except Exception as e:
        print(f"[ERROR] CVE fetch failed: {e}")


def analyze_cms(url):
    url = "http://" + url
    print(f"\n🔎 Scanning {url} for CMS fingerprint...")
    whatweb_output = run_whatweb(url)
    cms_versions = extract_cms_versions(whatweb_output)

    if not cms_versions:
        print("[-] No CMS detected.")
        return

    for cms, version in cms_versions:
        latest = latest_cms_versions.get(cms)
        if version:
            if latest and compare_versions(version, latest):
                print(f"[✅] {cms} detected (v{version}) — Up to date.")
            elif latest:
                print(f"[⚠️] {cms} outdated: v{version} < latest v{latest}")
                fetch_cves(cms, version)
            else:
                print(f"[❓] {cms} detected (v{version}) — Unknown latest version.")
                fetch_cves(cms, version)
        else:
            print(f"[❓] {cms} detected — version not exposed.")
            fetch_cves(cms, "unknown")
