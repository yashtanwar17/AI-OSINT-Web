from whois import whois
from datetime import datetime

def check_domain_expiration(domain, days_threshold=30):
    try:
        w = whois(domain)
        expiration_date = w.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if expiration_date is None:
            print(f"Could not find expiration date for {domain}")
            return

        current_date = datetime.now()
        days_until_expiration = (expiration_date - current_date).days

        if days_until_expiration < 0:
            print(f"The domain {domain} has already expired.")
        elif days_until_expiration <= days_threshold:
            print(f"The domain {domain} is close to expiration ({days_until_expiration} days left).")
        else:
            print(f"The domain {domain} is active. {days_until_expiration} days until expiration.")
    except Exception as e:
        print(f"Error fetching WHOIS data for {domain}: {e}")

