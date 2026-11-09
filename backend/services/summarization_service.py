from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from backend.model.all import summarize_model
from backend.services.vector_service import get_full_content

map_prompt = PromptTemplate.from_template(
    """Summarize this excerpt from a video transcript. Use only information stated
in the excerpt. Capture its main ideas and important supporting details without
adding outside knowledge.

Transcript excerpt:
{text}

Excerpt summary:"""
)

combine_prompt = PromptTemplate.from_template(
    """Write a clear, concise summary of the video using only the transcript
summaries below. Combine repeated ideas, preserve important details and
relationships between ideas, and do not add information that is not present.

Transcript summaries:
{text}

Video summary:"""
)

summarize_chain = load_summarize_chain(
    llm=summarize_model,
    chain_type="map_reduce",
    map_prompt=map_prompt,
    combine_prompt=combine_prompt,
)


def summarize_video(video_id: str) -> str:
    documents = get_full_content(video_id=video_id)

    if not documents:
        raise ValueError(
            f"No transcript documents found for {video_id}"
        )

    result = summarize_chain.invoke({
        "input_documents": documents
    })

    return result["output_text"]
