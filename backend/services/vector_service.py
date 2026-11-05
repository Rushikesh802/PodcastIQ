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


COLLECTION_NAME = 'yt-script'
client = QdrantClient(url=url, api_key=api_key)


@lru_cache(maxsize=1)
def get_vector_store() -> QdrantVectorStore:
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=3072,
                distance=models.Distance.COSINE,
            ),
        )
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embed_model,
    )

def get_full_content() -> Document:
    records, next_page = client.scroll(
        collection_name=COLLECTION_NAME,
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

def clean_vector_store():
    vs = get_vector_store()
    vs.delete_collection()
