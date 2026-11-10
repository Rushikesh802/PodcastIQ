import logging
from fastapi.responses import StreamingResponse
import httpx
from fastapi import APIRouter, HTTPException, status
from backend.services.generation_service import final_output

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/chat')
async def chat(query: str, video_id: str):

    async def generate():
        try:
            async for chunk in final_output(user_query=query, video_id=video_id):
               
                    yield chunk

        except Exception:
            logger.exception(
                "Streaming failed for video_id=%s",
                video_id
            )
            raise


    return StreamingResponse(
        generate(),
        media_type='text/plain',
         headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
