from langchain_classic.chains.summarize import load_summarize_chain
from backend.model.all import chat_model
from backend.services.vector_service import get_full_content

summarize_chain = load_summarize_chain(
    llm=chat_model,
    chain_type="map_reduce"
)


def summarize_video(video_id: str) -> str:
    documents = get_full_content(collection_name=video_id)

    if not documents:
        raise ValueError(
            f"No transcript documents found for {video_id}"
        )

    result = summarize_chain.invoke({
        "input_documents": documents
    })

    return result["output_text"]
