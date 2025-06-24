import dns.resolver

# Common DKIM selectors
dkim_selectors = [
    "default",
    "selector1",
    "selector2",
    "google",
    "mail",
    "smtp",
    "dkim",
    "email",
    "mx",
    "key1",
    "key2",
    "sig1",
    "sig2",
    "sendgrid",
    "mandrill",
    "mailgun",
    "zoho",
    "office365",
    "amazonses",
    "mta",
    "postfix",
    "exim",
    "fastmail",
    "protonmail",
    "gapps",
    "server",
    "webmail",
    "gateway",
    "newsmtp",
    "relay",
    "mg",
    "sp",
    "p1",
    "default1",
    "dkim1",
    "s1",
    "d1",
    "mail1",
    "s1024",
    "selector",
    "custom"
]


def check_dkim(domain, selectors=dkim_selectors):
    found = False
    print(f"\n🔍 Checking DKIM records for {domain}...\n")
    for selector in selectors:
        dkim_domain = f"{selector}._domainkey.{domain}"
        try:
            answers = dns.resolver.resolve(dkim_domain, 'TXT')
            for rdata in answers:
                record = str(rdata.to_text().strip('"'))
                if "v=DKIM1" in record:
                    print(f"[FOUND] {dkim_domain}:\n  {record}\n")
                    found = True
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            continue
        except Exception as e:
            print(f"[ERROR] {dkim_domain}: {e}")

    if not found:
        print("[MISSING] No DKIM records found for any common selector.")

