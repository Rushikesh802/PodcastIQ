import re

from backend.schemas.chat import augmentation_prompt
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from backend.services.retrieval_service import get_retrieval_chain
from backend.services.summarization_service import summarize_video


str_parser = StrOutputParser()

SUMMARY_INTENT_PATTERNS = (
    re.compile(r"\b(?:summar(?:y|ies|ize|ise|izing|ising|ized|ised))\b"),
    re.compile(r"\b(?:overview|recap|tl\s*;?\s*dr)\b"),
    re.compile(r"\b(?:key|main|important)\s+(?:points|takeaways|highlights)\b"),
    re.compile(r"\b(?:main|key)\s+ideas\b"),
    re.compile(r"\bin\s+a\s+nutshell\b"),
    re.compile(r"\bwhat(?:'s| is)\s+(?:this|the)\s+(?:video|podcast)\s+about\b"),
    re.compile(r"\btell\s+me\s+about\s+the\s+(?:video|podcast)\b"),
)


def is_summary_request(query: str) -> bool:
    normalized_query = " ".join(query.casefold().split())
    return any(pattern.search(normalized_query) for pattern in SUMMARY_INTENT_PATTERNS)


# important default rag chain
def genrate_rag_answer(inputs: dict):

    rag_chain = get_retrieval_chain(video_id=inputs['video_id']) | augmentation_prompt | chat_model | str_parser

    return rag_chain.invoke({'query': inputs['query']})

rag_runnable = RunnableLambda(genrate_rag_answer)


def final_output(user_query: str, video_id: str):
    if is_summary_request(user_query):
        return summarize_video(video_id=video_id)

    return rag_runnable.invoke({
        'query': user_query,
        'video_id': video_id,
    })
