from googlesearch import search
import re

def find_emails_with_dorks(domain, num_results=20):
    query = f'site:{domain} "@{domain}"'
    results = search(query, num_results=num_results, lang="en")
    
    email_regex = r'[a-zA-Z0-9._%+-]+@' + re.escape(domain)
    found_emails = set()

    for url in results:
        try:
            import requests
            r = requests.get(url, timeout=5)
            matches = re.findall(email_regex, r.text)
            found_emails.update(matches)
        except:
            continue

    return list(found_emails)

