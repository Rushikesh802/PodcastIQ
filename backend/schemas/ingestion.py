
from pydantic import BaseModel, Field, HttpUrl


class IngestionRequest(BaseModel):
    url: HttpUrl
