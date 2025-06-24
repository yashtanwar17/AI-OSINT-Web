import tldextract, whois
import dns.resolver
import socket
import itertools

adjacent_keys = {
    'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'erfcxs', 'e': 'wsdr',
    'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg', 'i': 'ujko', 'j': 'uikmnh',
    'k': 'iolmj', 'l': 'opk', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx'
}

homoglyphs = {
    'o': ['0'], 'l': ['1', 'i'], 'i': ['1', 'l'], 'e': ['3'],
    'a': ['@'], 's': ['5', '$'], 'g': ['9'], 'b': ['8']
}

def generate_typos(domain):
    variants = set()
    domain = domain.lower()

    for i in range(len(domain)):
        variants.add(domain[:i] + domain[i+1:])

    for i in range(len(domain) - 1):
        swapped = list(domain)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add("".join(swapped))

    for i, char in enumerate(domain):
        if char in adjacent_keys:
            for adj in adjacent_keys[char]:
                variant = domain[:i] + adj + domain[i+1:]
                variants.add(variant)

    for i, char in enumerate(domain):
        if char in homoglyphs:
            for rep in homoglyphs[char]:
                variant = domain[:i] + rep + domain[i+1:]
                variants.add(variant)

    return variants

def is_registered(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def typosquatting_scan(target_domain):
    ext = tldextract.extract(target_domain)
    base = ext.domain
    tld = ext.suffix
    print(f"[~] Generating typosquatting domains for: {base}.{tld}")

    typos = generate_typos(base)
    results = []

    for typo in typos:
        typo_domain = f"{typo}.{tld}"
        if is_registered(typo_domain):
            print(f"[!] Possible typosquatting domain active: {typo_domain}")
          
          
            results.append(typo_domain)

    if not results:
        print("[✓] No active typosquatting domains found.")
    return results

