from fastapi import FastAPI
from backend.api import  ingestion

app = FastAPI(title='PodcastIQ')


@app.get('/')
def home():
    return {'message': 'Welcome to PodcastIQ, Your Yt summarization app'}

@app.get('/health')
def health():
    return {'message': 'api working fine',
            'metadata': {
                'status_code': 200,
                'Developer': 'Rushikesh Patil'
            }}


#routing files

# Query endpoint


# Data Ingestion endpoint
app.include_router(ingestion.router)



