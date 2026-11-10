
import os

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from backend.model.all import embed_model


url = os.getenv("QUDRANT_URL")
api_key = os.getenv("QUDRANT_API_KEY")

client = QdrantClient(
    url=url,
    api_key=api_key,
    timeout=120,
)


def get_vector_store(video_id: str) -> QdrantVectorStore:

    if not client.collection_exists(collection_name=video_id):
        client.create_collection(
            collection_name=video_id,
            vectors_config=models.VectorParams(
                size=2048,
                distance=models.Distance.COSINE,
            ),
        )

    return QdrantVectorStore(
        client=client,
        collection_name=video_id,
        embedding=embed_model,
    )


def get_full_content(video_id: str) -> list[Document]:

    if not client.collection_exists(collection_name=video_id):
        return []

    records = []
    offset = None

    while True:
        page, next_page = client.scroll(
            collection_name=video_id,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        records.extend(page)

        if next_page is None:
            break

        offset = next_page

    documents = [
        Document(
            page_content=record.payload.get("page_content", ""),
            metadata=record.payload.get("metadata", {}),
        )
        for record in records
        if record.payload
    ]

    return documents


def clean_vector_store(video_id: str):

    if client.collection_exists(collection_name=video_id):
        client.delete_collection(collection_name=video_id)
