from backend.services.generation_service import final_output

URL = 'https://youtu.be/'

def index_base():

    from backend.services.transcript_service import load_youtube_transcript, manual_loader
    from backend.services.chunking_service import chunking
    from backend.services.vector_service import vectore_store

    # transcript = load_youtube_transcript(url=URL)

    transcript = manual_loader()
   
    chunking_data = chunking(transcript)

    vectore_store.add_documents(chunking_data)



print(final_output(user_query='summarize the video', video_id=425))


