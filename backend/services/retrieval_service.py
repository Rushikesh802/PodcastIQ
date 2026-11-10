from operator import itemgetter
from langchain_core.runnables import RunnableParallel, RunnableLambda
from backend.services.vector_service import get_vector_store


def format_retrieved_docs(retrieved_docs):

    content = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    metadata = (
        retrieved_docs[0].metadata
        if retrieved_docs else {}
    )

    return {
        "content": content,
        "metadata": metadata,
    }


def flatten_retrieval_context(retrieval_result):
    context = retrieval_result["context"]

    return {
        "video_metadata": context["metadata"],
        "transcript_context": context["content"],
        "query": retrieval_result["query"],
    }


def get_retrieval_chain(video_id: str):

    retriever = get_vector_store(
        video_id=video_id
    ).as_retriever(
        search_kwargs={"k": 6}
    )

    return (
        RunnableParallel({
            "context": (
                itemgetter("query")
                | retriever
                | RunnableLambda(format_retrieved_docs)
            ),
            "query": itemgetter("query"),
        })
        | RunnableLambda(flatten_retrieval_context)
    )
