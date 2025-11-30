import re
from urllib.parse import parse_qs, urlparse


def extract_youtube_id(url: str) -> str | None:
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url):
        return url

    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()

    # youtu.be/<id>
    if host in ("youtu.be", "www.youtu.be"):
        video_id = parsed.path.lstrip("/")
        video_id = video_id.split("/")[0]
        return video_id or None

    # youtube.com
    if any(h in host for h in ("youtube.com", "youtube-nocookie.com")):
        path = parsed.path

        # https://www.youtube.com/watch?v=...
        if path == "/watch":
            qs = parse_qs(parsed.query)
            video_id = qs.get("v", [None])[0]
            return video_id

        # /embed/<id>, /shorts/<id>, /v/<id>, /live/<id>
        for prefix in ("/embed/", "/shorts/", "/v/", "/live/"):
            if path.startswith(prefix):
                parts = path.split("/")
                if len(parts) >= 3 and parts[2]:
                    return parts[2]

    # fallback
    m = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)

    return None
