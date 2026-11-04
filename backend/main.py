from backend.services.transcript_service import load_youtube_transcript, manual_loader
from backend.services.chunking_service import chunking
from backend.services.vector_service import vectore_store

URL = 'https://youtu.be/B6PMiwqu_18?si=1U9reASPNhNa_noD'

## indexing part


# print(transcript)


def index_base(url):
    # 1. transcipit script of youtube url
    # transcript = load_youtube_transcript(url=URL)

    ## temporary manually load the data

    transcript = manual_loader()
    chunking_data = chunking(transcript)
    
    # vectore_store
    vectore_store.add_documents(chunking_data)

# transcript = load_youtube_transcript(url=URL)
# print(transcript)





