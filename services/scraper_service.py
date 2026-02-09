import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Educational Research Bot)"
}


BLOCKED_KEYWORDS = {"login", "signup", "privacy", "ads"}


def scrape_links(page_url: str, limit: int=10) -> list[str]:

    try:

        response = requests.get(
            page_url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()


        soup = BeautifulSoup(response.text, "html.parser")
        links = set()


        for a in soup.find_all("a", href=True):
            
            full_url = urljoin(page_url, a["href"])
            parsed = urlparse(full_url)

            if parsed.scheme not in {"http", "https"}:
                continue

            if any(word in full_url.lower() for word in BLOCKED_KEYWORDS):
                continue

            links.add(full_url)

            if len(links) >= limit:
                break

        return list(links)
    
    except Exception as e:
        logging.warning(f"Scraping failed for {page_url}: {e}")
        return []
    