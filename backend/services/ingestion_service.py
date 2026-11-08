from backend.services.transcript_service import load_youtube_transcript
from backend.services.chunking_service import chunking
from backend.services.vector_service import get_vector_store



def ingest_data(url: str):
    print('Ingestion process initialize.......')
    transcript = load_youtube_transcript(url=url)
    print('Step: 1. Completed: Transcript run module run successfully!!')
    chunking_data = chunking(transcript.page_content)
    print('Step: 2. Completed: data chunking successfully!!')
    vs = get_vector_store(collection_name=transcript.metadata['video_id'])
    print(f'Step: 3. Completed:vector database access succssfully with collection name: {transcript.metadata['video_id']}')
    vs.add_documents(documents=chunking_data, batch_size=32)
    print(f'Step: 4. Completed: Data added in QDRANT succssfully with Collection name: {transcript.metadata['video_id']}')

ingest_data(url='https://youtu.be/RR2bORcvzKs?si=EfXT4zzz5U8asCSZ')


    
