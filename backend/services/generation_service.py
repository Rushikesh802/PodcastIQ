import asyncio
import re

from backend.schemas.chat import augmentation_prompt
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from backend.services.retrieval_service import get_retrieval_chain


str_parser = StrOutputParser()


# important default rag chain
def genrate_rag_answer(inputs: dict):

    rag_chain = get_retrieval_chain(video_id=inputs['video_id']) | augmentation_prompt | chat_model | str_parser

    return rag_chain.invoke({'query': inputs['query']})

rag_runnable = RunnableLambda(genrate_rag_answer)


def final_output(user_query: str, video_id: str) -> str:
    return rag_runnable.invoke({
            'query': user_query,
            'video_id': video_id,
        })
