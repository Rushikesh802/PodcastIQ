from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()

embed_model = GoogleGenerativeAIEmbeddings(model='gemini-embedding-2')

# chat_model = ChatOpenRouter(model='nvidia/nemotron-3-ultra-550b-a55b:free')

chat_model = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')
