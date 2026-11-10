from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from dotenv import load_dotenv

load_dotenv()

embed_model = init_embeddings(provider='cohere', model='embed-v5.0-fast')

chat_model = init_chat_model(model_provider='mistralai', model='ministral-3b-2512', streaming=True)


