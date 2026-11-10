from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from urllib.parse import urlparse, parse_qs
from yt_dlp import YoutubeDL


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.strip("/").split("/")[0]

    if parsed.path == "/watch":
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            return video_id

    if parsed.path.startswith(("/shorts/", "/embed/")):
        return parsed.path.split("/")[2]

    raise ValueError("Invalid YouTube URL")


def get_video_metadata(url: str) -> dict:
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "video_id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "channel": info.get("channel"),
        "channel_id": info.get("channel_id"),
        "channel_url": info.get("channel_url"),
        "uploader": info.get("uploader"),
        "uploader_id": info.get("uploader_id"),
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "duration_string": info.get("duration_string"),
        "thumbnail": info.get("thumbnail"),
        "thumbnails": info.get("thumbnails"),
        "tags": info.get("tags") or [],
        "categories": info.get("categories") or [],
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "language": info.get("language"),
        "webpage_url": info.get("webpage_url"),
        "age_limit": info.get("age_limit"),
        "availability": info.get("availability"),
    }



def load_youtube_transcript(url: str) -> Document:
    video_id = extract_video_id(url)

    # Extract video metadata
    metadata = get_video_metadata(url)

    # Supported transcript languages
    supported_languages = [
        "en",       # English
        "hi",       # Hindi
        "mr",       # Marathi
        "en-US",
        "en-GB",
        "hi-IN",
        "mr-IN",
    ]

    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id,
        languages=supported_languages
    )

    transcript_text = " ".join(
        snippet.text for snippet in transcript
    )

    # Actual transcript language
    transcript_language = getattr(
        transcript,
        "language_code",
        None
    )

    metadata.update({
        "source": url,
        "video_id": video_id,
        "transcript_language": transcript_language,
        "transcript_language_name": getattr(
            transcript, "language", None
        ),
        "transcript_is_generated": getattr(
            transcript, "is_generated", None
        ),
        "transcript_available": bool(transcript_text),
    })

    return Document(
        page_content=transcript_text,
        metadata=metadata,
    )
