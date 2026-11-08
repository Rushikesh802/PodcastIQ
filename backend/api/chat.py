import logging

import httpx
from fastapi import APIRouter, HTTPException, status
from backend.services.generation_service import final_output

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/chat')
def chat(query: str, video_id: str) -> str:
    try:
        return final_output(user_query=query, video_id=video_id)

    except Exception as e:
        logger.exception("Chat generation failed for video_id=%s", video_id)
        if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 429:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail='The Mistral API rate limit has been reached. Wait before trying again.',
            ) from e
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Chat generation failed. Check the backend logs for details.') from e

