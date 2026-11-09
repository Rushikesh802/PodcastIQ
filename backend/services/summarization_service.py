import asyncio
import logging
from time import perf_counter

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.schemas.chat import map_prompt, reduce_prompt
from backend.model.all import summarize_model
from backend.services.vector_service import get_full_content

logger = logging.getLogger(__name__)

MAX_CONCURRENCY = 5

map_chain = map_prompt | summarize_model | StrOutputParser()
reduce_chain = reduce_prompt | summarize_model | StrOutputParser()


async def summarize_video(video_id: str) -> str:
    start = perf_counter()

    documents = await asyncio.to_thread(
        get_full_content,
        video_id=video_id
    )

    if not documents:
        raise ValueError(f"No transcript found: {video_id}")

    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async def map_document(document):
        async with semaphore:
            return await map_chain.ainvoke({
                "text": document.page_content
            })

    map_start = perf_counter()

    summaries = await asyncio.gather(
        *(map_document(doc) for doc in documents)
    )

    map_duration = perf_counter() - map_start

    reduce_start = perf_counter()

    final_summary = await reduce_chain.ainvoke({
        "text": "\n\n".join(summaries)
    })

    reduce_duration = perf_counter() - reduce_start

    logger.info(
        "Summarization | chunks=%d | map=%.2fs | "
        "reduce=%.2fs | total=%.2fs",
        len(documents),
        map_duration,
        reduce_duration,
        perf_counter() - start
    )

    return final_summary
