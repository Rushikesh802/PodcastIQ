from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from model.all import embed_model
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('QUDRANT_URL')
api_key = os.getenv('QUDRANT_API_KEY')



client = QdrantClient(url=url,
                      api_key=api_key )

COLLECTION_NAME = 'yt-script'
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=3072,
            distance=models.Distance.COSINE,
        ),
    )

# Initialize vector store
vectore_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embed_model,
)


