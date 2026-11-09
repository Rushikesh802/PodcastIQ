from fastapi import APIRouter
from backend.services.vector_service import clean_vector_store


router = APIRouter()


@router.delete('/delete')
def clean_collection(video_id: str):
    
    return clean_vector_store(video_id=video_id)
