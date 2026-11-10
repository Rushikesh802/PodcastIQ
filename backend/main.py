from fastapi import FastAPI
from backend.api import ingestion, chat, clean_collection

app = FastAPI(
    title="PodcastIQ",
    description="YouTube Video Q&A Application",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to PodcastIQ, Your long video Q&A app"
    }


@app.get("/health")
def health():
    return {
        "message": "API working fine",
        "status": "healthy"
    }


app.include_router(chat.router)
app.include_router(ingestion.router)
app.include_router(clean_collection.router)
