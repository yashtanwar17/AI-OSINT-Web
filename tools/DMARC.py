import dns.resolver

def check_dmarc(domain):
    dmarc_domain = f"_dmarc.{domain}"
    try:
        answers = dns.resolver.resolve(dmarc_domain, "TXT")
        for rdata in answers:
            record = str(rdata.to_text().strip('"'))
            if "v=DMARC1" in record:
                print(f"[FOUND] DMARC record for {domain}:")
                print(record)
                return
        print(f"[MISSING] No valid DMARC record found for {domain}.")
    except dns.resolver.NXDOMAIN:
        print(f"[MISSING] No DMARC DNS record (NXDOMAIN) for {domain}.")
    except dns.resolver.NoAnswer:
        print(f"[MISSING] No DMARC DNS answer for {domain}.")
    except dns.resolver.Timeout:
        print(f"[TIMEOUT] DNS query timed out for {domain}.")
    except Exception as e:
        print(f"[ERROR] Could not check DMARC for {domain}: {e}")

