import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.schemas.chat import ChatRequest
from backend.services.generation_service import final_output


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat")
async def chat(request: ChatRequest):

    async def generate():

        try:
            async for chunk in final_output(
                user_query=request.query,
                video_id=request.video_id
            ):
                yield chunk

        except Exception:
            logger.exception(
                "Streaming failed for video_id=%s",
                request.video_id
            )
            raise

    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
