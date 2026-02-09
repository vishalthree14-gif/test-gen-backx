from services.search_service import search_web
from services.scraper_service import scrape_links

def get_learning_resource(topic: str, max_pages: int = 5) -> list[str]:

    urls = search_web(topic, max_pages)
    resources = set()

    for url in urls:
        for link in scrape_links(url):
            resources.add(link)

    return list(resources)[:20]

