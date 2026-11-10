from backend.services.transcript_service import load_youtube_transcript
from backend.services.chunking_service import chunking
from backend.services.vector_service import get_vector_store


def ingest_data(url: str):
    print("Ingestion process initialized...")

    # Step 1: Extract transcript + video metadata
    transcript = load_youtube_transcript(url=url)
    video_id = transcript.metadata["video_id"]

    print("Step 1: Transcript and metadata extracted successfully!")

    # Step 2: Chunk transcript while preserving metadata
    chunking_data = chunking(document=transcript)

    print("Step 2: Transcript chunking completed!")

    # Step 3: Access vector store
    vs = get_vector_store(video_id=video_id)

    print(f"Step 3: Connected to Qdrant collection: {video_id}")

    # Step 4: Store chunks and metadata
    vs.add_documents(
        documents=chunking_data,
        batch_size=16
    )

    print(f"Step 4: Documents added successfully to {video_id}")

    return video_id
