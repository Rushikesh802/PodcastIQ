from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()

embed_model = GoogleGenerativeAIEmbeddings(model='gemini-embedding-2')

chat_model = ChatOpenRouter(model='nvidia/nemotron-3-ultra-550b-a55b:free')

