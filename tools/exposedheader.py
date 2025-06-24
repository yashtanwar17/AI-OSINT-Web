import requests

sensitive_headers = [
    "Server",
    "X-Powered-By",
    "X-AspNet-Version",
    "X-AspNetMvc-Version",
    "X-Pingback",
    "X-Drupal-Cache",
    "X-Generator",
    "X-Backend-Server",
    "X-Envoy-Upstream-Service-Time",
    "X-Version",
    "X-Served-By",
    "Via",
    "X-Cloud-Trace-Context",
    "X-Amz-Cf-Id",
    "X-Amz-Request-Id",
    "X-Amzn-Trace-Id",
    "CF-Cache-Status",
    "CF-RAY",
    "X-Request-ID",
    "X-Forwarded-Server",
    "X-Forwarded-Host",
    "X-Forwarded-For",
    "X-HW",
    "X-Powered-CMS",
    "X-Wix-Request-Id",
    "X-Turbo-Charged-By",
    "X-Varnish",
    "X-Akamai-Transformed",
    "X-Mod-Pagespeed",
    "X-Cache",
    "X-Hostname"
]

def check_headers(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
    except Exception as e:
        print(f"[ERROR] Failed to fetch headers for {url}: {e}")
        return

    headers = response.headers
    print(f"\n🔍 Headers exposed by {url}:\n")
    found = False
    for header, value in headers.items():
        if header in sensitive_headers:
            print(f"[EXPOSED] {header}: {value}")
            found = True
    if not found:
        print("✅ No known sensitive headers exposed.")

if __name__ == "__main__":
    target = "mit.edu"
    check_headers(target)
