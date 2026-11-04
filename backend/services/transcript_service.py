import re
from youtube_transcript_api import YouTubeTranscriptApi


# extract the video id from youtube URL
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|live/)([a-zA-Z0-9_-]{11})", url)

    if match:
        return match.group(1)

    raise ValueError("Invalid YouTube URL")


def script_fetcher(url):

    video_id = extract_video_id(url=url)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcrpit = ytt_api.fetch(video_id=video_id)

        return transcrpit
    
    except : {'message': 'Youtube have some issue errror'}
