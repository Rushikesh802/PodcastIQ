from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

embed_model = GoogleGenerativeAIEmbeddings(model='gemini-embedding-2')

chat_model = ChatMistralAI(model='ministral-3b-2512')

# chat_model = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')
