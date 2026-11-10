import logging

from fastapi import APIRouter, HTTPException, status

from backend.schemas.ingestion import IngestionRequest
from backend.services.ingestion_service import ingest_data


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/data_ingestion",
    status_code=status.HTTP_201_CREATED
)
def index_base(request: IngestionRequest):

    try:
        video_id = ingest_data(url=str(request.url))

        return {
            "success": True,
            "message": "Data ingestion successfully completed!",
            "video_id": video_id
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        logger.exception("Data ingestion failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data ingestion failed. Check backend logs."
        ) from exc
