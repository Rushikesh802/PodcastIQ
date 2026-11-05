URL = 'https://youtu.be/k0Ka-deab1s?si=_OY4G7_p0eF1PbAS'

def index_base():

    from backend.services.transcript_service import load_youtube_transcript
    from backend.services.chunking_service import chunking
    from backend.services.vector_service import vectore_store

    transcript = load_youtube_transcript(url=URL)
   
    chunking_data = chunking(transcript.page_content)

    vectore_store.add_documents(chunking_data)
