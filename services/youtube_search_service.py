from ddgs import DDGS
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)

    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    return None


def search_youtube_videos(topic: str, max_results:int = 8) -> list[dict]:

    query = f"{topic} tutorial site:youtube.com"

    videos = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for r in results:
            url = r.get("href", "")
            title = r.get("title", "")

            video_id = extract_video_id(url)

            if not video_id:
                continue

            videos.append({
                "title":title,
                "url": url,
                "video_id": video_id
            })

    return videos