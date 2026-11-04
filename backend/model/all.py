from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embed_model = GoogleGenerativeAIEmbeddings(model='gemini-embedding-2')

