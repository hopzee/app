import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_official_urls(base_url, allowed_domains=None):
    """Scrape official URLs from a given portal. Optionally filter by allowed domains."""
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Failed to fetch {base_url}: {e}")
        return set()

    soup = BeautifulSoup(response.text, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        parsed = urlparse(href)
        domain = parsed.netloc.lower()
        if domain != "":
            if allowed_domains:
                if any(d in domain for d in allowed_domains):
                    links.add(domain)
            else:
                links.add(domain)
    return links

# Example usage
allowed = [".gov.ng", ".mil.ng", ".org", ".edu.ng", ".com.ng"]
gov_urls = set()
gov_urls.update(scrape_official_urls("https://services.gov.ng", allowed))
gov_urls.update(scrape_official_urls("https://foia.justice.gov.ng/index.php?Itemid=139&id=24&lang=en", allowed))
gov_urls.update(scrape_official_urls("https://www.nipc.gov.ng/compendium/7-addresses-of-relevant-government-agencies/", allowed))

print(f"Found {len(gov_urls)} official domains:")
print(gov_urls)
