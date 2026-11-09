import logging

from fastapi import APIRouter, HTTPException, status
from backend.services.ingestion_service import ingest_data

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/data_ingestion', status_code=status.HTTP_201_CREATED)
def index_base(url: str):
    try:
        video_id = ingest_data(url=url)
        return {'response': 'Data ingestion successefully!!',
                'video_id': video_id}

    except Exception as exc:
        logger.exception("Data ingestion failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Data ingestion failed. Check the backend logs for details.',
        ) from exc
