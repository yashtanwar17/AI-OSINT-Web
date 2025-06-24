from tools import dirscan, DKIM, DMARC, employee, expireddomain, exposedheader, filescannerweb, googleemaildork, haveipwnedtest, jsscanner, outdatedcmsandcve, outdatedwebserver, panelscanner, sdtakeover, SPF, sslscan, typosquatting, vulnportscanner, xsstest
import tempfile
import io
from contextlib import redirect_stdout

print("""
🔍 AI Web Scanner            
https://github.com/yashtanwar17/AI-OSINT-Web
""")

domain = input("Enter domain name (example.com): ")

log_file_path = "log.txt"

# Decorator for logging
def log_output(func):
    def wrapper(*args, **kwargs):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print(f"[>>] Running: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                if result:
                    print(f"[Return] {result}")
            except Exception as e:
                print(f"[!] {func.__name__} failed: {e}")
        output = buffer.getvalue()
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"\n[+] {func.__name__} Output:\n")
            f.write(output)
        print(output)  # Also show in console
    return wrapper

# Sub-functions wrapped with decorator
@log_output
def jscan(domainy):
    cdn_js_urls = jsscanner.fetch_cdn_js_urls(domainy)
    if not cdn_js_urls:
        print("[JS Scan] No JS URLs found.")
        return
    with tempfile.TemporaryDirectory() as temp_dir:
        jsscanner.download_js_files(cdn_js_urls, temp_dir)
        jsscanner.scan_with_retire(temp_dir)

@log_output
def gdork(domainx):
    x = googleemaildork.find_emails_with_dorks(domainx)
    print(f"[GDork] Found {len(x)} emails:")
    for email in x:
        print(f" - {email}")

# Main runner wrapped with logging
@log_output
def run_all():
    dirscan.scan_directory_listing(domain)
    DKIM.check_dkim(domain)
    DMARC.check_dmarc(domain)
    employee.run(domain)
    expireddomain.check_domain_expiration(domain)
    exposedheader.check_headers(domain)
    filescannerweb.scan_directory_listing(domain)
    gdork(domain)
    jscan(domain)
    outdatedcmsandcve.analyze_cms(domain)
    outdatedwebserver.check_server_version(domain)
    panelscanner.scan_admin_panels(domain)
    sdtakeover.scan(domain)
    SPF.check_spf(domain)
    sslscan.check_ssl(domain)
    typosquatting.typosquatting_scan(domain)
    print("[NOTE] : Custom ports cannot be scanned as this is not a fully operational NMAP scan.")
    vulnportscanner.scan_host(domain)
    xsstest.run_vuln_tests(domain)

# Run all
run_all()

print(f"\n[✓] All scan outputs saved to {log_file_path}")

from openai import OpenAI

client = OpenAI(
    api_key="004d9d81-50ae-4a63-854e-676ef6b725ba",
    base_url="https://api.sambanova.ai/v1",
)


# Step 1: Read the log.txt
with open("log.txt", "r", encoding="utf-8") as file:
    log_content = file.read()

# Step 2: Create a smart prompt for log analysis
prompt = f"""
You are a cybersecurity expert AI. Analyze the following scan output log and provide a clear, human-readable report with highlights of:
- Vulnerabilities
- Misconfigurations
- Exposed files or directories
- CMS issues or outdated software
- SSL/TLS or DNS problems
- Any recommendations for remediation

Log:
{log_content}
"""

# Step 3: Send to SambaNova AI
response = client.chat.completions.create(
    model="DeepSeek-R1-0528",
    messages=[
        {"role": "system", "content": "You are a cybersecurity assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    top_p=0.9,
)

# Step 4: Get the AI's response
ai_report = response.choices[0].message.content

# Step 5: Save to ailog.txt
with open("ailog.txt", "w", encoding="utf-8") as out_file:
    out_file.write(ai_report)

print("AI report saved to 'ailog.txt'")
