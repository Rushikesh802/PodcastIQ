from operator import itemgetter
from langchain_core.runnables import RunnableParallel, RunnableLambda
from backend.services.vector_service import get_vector_store


def format_docs(retrieved_docs):
    return "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )
    

def get_retrieval_chain(video_id: str):
    retriever = get_vector_store(video_id=video_id).as_retriever(
        search_kwargs={'k': 3}
    )


    return RunnableParallel({
        'content': itemgetter('query') | retriever | RunnableLambda(format_docs),
        'query': itemgetter('query')
    })

   