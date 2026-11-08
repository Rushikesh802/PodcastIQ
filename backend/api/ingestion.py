from fastapi import APIRouter, HTTPException, status
from backend.services.ingestion_service import ingest_data

router = APIRouter()


@router.post('/data_ingestion', status_code=status.HTTP_201_CREATED)
def index_base(url: str):
    try:
        video_id = ingest_data(url=url)
        return {'response': 'Data ingestion successefully!!',
                'video_id': video_id}

    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                            detail='Data ingestion failed Internal server have facing some issuse maybe long video time out!')