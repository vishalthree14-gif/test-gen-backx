from ddgs import DDGS

def search_web(topic: str, max_results: int = 5) -> list[str]:

    if not topic:
        return []
    
    urls = []

    with DDGS() as ddgs:
        results = ddgs.text(
            f"{topic} tutorial explanation",
            max_results=max_results
        )

        for r in results:
            if "href" in r:
                urls.append(r["href"])

    return urls
