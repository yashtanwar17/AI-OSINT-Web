import dns.resolver

def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            txt_record = str(rdata.to_text().strip('"'))
            if txt_record.startswith("v=spf1"):
                print(f"[SPF FOUND] {txt_record}")
                return
        print("[SPF MISSING] No SPF record found.")
    except Exception as e:
        print(f"[SPF ERROR] {e}")


