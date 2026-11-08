from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from backend.model.all import embed_model
from dotenv import load_dotenv
from functools import lru_cache
import os

load_dotenv()

url = os.getenv('QUDRANT_URL')
api_key = os.getenv('QUDRANT_API_KEY')


client = QdrantClient(url=url,
                      api_key=api_key,
                      timeout=40)



def get_vector_store(collection_name: str) -> QdrantVectorStore:
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=3072,
                distance=models.Distance.COSINE,
            ),
        )
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embed_model,
    )

def get_full_content(collection_name: str) -> Document:
    records, next_page = client.scroll(
        collection_name=collection_name,
        limit=100,
        with_payload=True,
        with_vectors=False
    )

    documents = [
        Document(
            page_content=record.payload['page_content'],
            )
        for record in records
    ]

    return documents

def clean_vector_store(video_id: str):
    if client.collection_exists(video_id):
        client.delete_collection(collection_name=video_id)
