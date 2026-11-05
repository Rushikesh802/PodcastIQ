from fastapi import FastAPI

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