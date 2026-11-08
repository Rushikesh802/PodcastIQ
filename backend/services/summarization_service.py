import logging

from langchain_classic.chains.summarize import load_summarize_chain
from backend.model.all import chat_model
from backend.services.vector_service import get_full_content
from backend.services.cache_service import (
    get_cached_summary,
    cache_summary
)

logger = logging.getLogger(__name__)

summarize_chain = load_summarize_chain(
    llm=chat_model,
    chain_type="map_reduce"
)


def summarize_video(video_id: str) -> str:

    # 1. Check Redis
    cached_summary = get_cached_summary(video_id)

    if cached_summary:
        logger.info("Summary cache hit: %s", video_id)
        return cached_summary

    logger.info("Summary cache miss: %s", video_id)

    # 2. Fetch all transcript documents
    documents = get_full_content(video_id=video_id)

    if not documents:
        raise ValueError(
            f"No transcript documents found for {video_id}"
        )

    # 3. Generate summary
    result = summarize_chain.invoke({
        "input_documents": documents
    })

    summary = result["output_text"]

    # 4. Cache summary
    cache_summary(
        video_id=video_id,
        summary=summary
    )

    return summary
