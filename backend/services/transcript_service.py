from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from langchain_core.documents import Document
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()

def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.strip("/")

    if parsed.path == "/watch":
        return parse_qs(parsed.query).get("v", [None])[0]

    if parsed.path.startswith("/shorts/"):
        return parsed.path.split("/")[2]

    raise ValueError("Invalid YouTube URL")


def load_youtube_transcript(url: str) -> Document:
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username=os.getenv("WEBSHARE_PROXY_USERNAME"),
            proxy_password=os.getenv("WEBSHARE_PROXY_PASSWORD"),
        )
    )
    
    transcript = api.fetch(video_id, languages=["en"])

    text = " ".join(
        snippet.text for snippet in transcript
    )

    return Document(
        page_content=text,
        metadata={
            "source": url,
            "video_id": video_id,
            "language": "en",
        },
    )




def manual_loader():
    with open('backend\services\s.txt', 'r') as f:
        data = f.read()

    return data

