from pydantic import BaseModel, Field
from typing import Literal

class Query(BaseModel):
     query: Literal['summarize', 'other'] = Field(
        description="User intent: summarize the video or other query"
    )

