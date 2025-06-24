import csv
import time
from bs4 import BeautifulSoup
from googlesearch import search
import requests

def google_dork_linkedin(company_name, limit=10):
    query = f'site:linkedin.com/in/ AND "{company_name}"'
    print(f"[~] Searching for employees of: {company_name} (limit={limit})")

    try:
        results = list(search(query, num_results=limit))
        if len(results) < limit:
            print(f"[!] Only found {len(results)} results (limit was {limit})")
        return results
    except Exception as e:
        print(f"[x] Google Search failed: {e}")
        return []

def extract_profile_info(link):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(link, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("title").text.strip()
        description = soup.find("meta", {"name": "description"})
        desc = description["content"] if description else "N/A"

        return title, desc
    except Exception as e:
        return "N/A", "N/A"

def run(company_name, limit=10):
    print(f"Note: LIMIT SET TO {limit} — increase for deeper analysis")
    links = google_dork_linkedin(company_name, limit)
    results = []

    for idx, link in enumerate(links):
        print(f"[{idx+1}] {link}")
        title, desc = extract_profile_info(link)
        print(f"     ↳ Title: {title}")
        print(f"     ↳ Description: {desc}")
        results.append([title, desc, link])
        time.sleep(1.5)  # avoid IP blocking

if __name__ == "__main__":
    company = "mit.edu"
    run(company, limit=10)
