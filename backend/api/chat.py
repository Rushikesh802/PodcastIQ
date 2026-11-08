from fastapi import APIRouter, HTTPException, status
from backend.services.generation_service import final_output

router = APIRouter()


@router.post('/chat')
def chat(q: str, video_id: str) -> str:
    try:
        return final_output(user_query=q, video_id=video_id)
        

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                             detail='Rag Service show some error!')



