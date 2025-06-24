import requests
import time
import dns.resolver
import socket

API_KEY = "6f24a9032bdb64da8734fa3a9e251900a84bbc0740b764b70927dd4a83f01f4d"  # 🔐 Replace with your actual key

TAKEOVER_SIGNATURES = {
    "github.io": "There isn't a GitHub Pages site here.",
    "herokuapp.com": "No such app",
    "amazonaws.com": "NoSuchBucket",
    "bitbucket.io": "Repository not found",
    "fastly.net": "Fastly error: unknown domain",
    "cloudfront.net": "Bad request",
    "surge.sh": "project not found",
}

def get_subdomains(domain):
    print(f"[~] Gathering subdomains for {domain} via DNSDumpster API...")
    try:
        url = f"https://api.dnsdumpster.com/domain/{domain}"
        headers = {"X-API-Key": API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return list(set([
                entry["host"]
                for group in data.values()
                if isinstance(group, list)
                for entry in group
                if "host" in entry
            ]))
        else:
            print(f"[!] API error {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"[!] Error querying DNSDumpster: {e}")
        return []

def get_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, "CNAME")
        for rdata in answers:
            return rdata.target.to_text().strip(".")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.LifetimeTimeout):
        return None
    except Exception:
        return None

def is_takeover_possible(subdomain, cname_target):
    try:
        response = requests.get(f"http://{subdomain}", timeout=5)
        body = response.text.lower()
        for service, signature in TAKEOVER_SIGNATURES.items():
            if service in cname_target and signature.lower() in body:
                return True, service
    except requests.RequestException:
        pass
    return False, None

def scan(domain):
    subdomains = get_subdomains(domain)
    if not subdomains:
        print("[x] No subdomains found.")
        return

    print("\n[~] Checking subdomains for takeover potential...\n")
    vulnerable = []

    for sub in subdomains:
        cname = get_cname(sub)
        if cname:
            print(f"[~] {sub} has CNAME -> {cname}")
            is_vuln, service = is_takeover_possible(sub, cname)
            if is_vuln:
                print(f"[!] Potential takeover detected on {sub} (CNAME to {service})")
                vulnerable.append((sub, cname))
            else:
                print(f"[✓] {sub} CNAME OK")
        else:
            print(f"[-] {sub} has no CNAME record.")
        time.sleep(2)  # Respect API rate limits

    if not vulnerable:
        print("\n[✓] No takeover risks found.")
    else:
        print("\n[!] Takeover risks found:")
        for sub, cname in vulnerable:
            print(f"    {sub} -> {cname}")


