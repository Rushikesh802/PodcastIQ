from fastapi import FastAPI
from backend.api import ingestion, chat, clean_collection

app = FastAPI(title='PodcastIQ')


@app.get('/')
def home():
    return {'message': 'Welcome to PodcastIQ, Your long video Q&A app'}

@app.get('/health')
def health():
    return {'message': 'api working fine',
            'metadata': {
                'status_code': 200,
                'Developer': 'Rushikesh Patil'
            }}


#routing files

# Query endpoint
app.include_router(chat.router)

# Data Ingestion endpoint
app.include_router(ingestion.router)

# collection data delte endpoint
app.include_router(clean_collection.router)

