from backend.schemas.chat import augmentation_prompt
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser
from backend.services.retrieval_service import get_retrieval_chain
from typing import AsyncIterator

str_parser = StrOutputParser()

async def final_output(user_query: str, video_id: str) -> AsyncIterator[str]:

    rag_chain = (get_retrieval_chain(video_id=video_id) | augmentation_prompt | chat_model | str_parser)

    async for chunk in rag_chain.astream({'query': user_query}):
        if chunk:
            yield chunk
