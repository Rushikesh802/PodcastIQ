from operator import itemgetter
from langchain_core.runnables import RunnableParallel, RunnableLambda
from backend.services.vector_service import get_vector_store


def format_docs(retrieved_docs):
    context_text = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )
    return context_text


retriever = get_vector_store().as_retriever(
    search_kwargs={'k': 3}
)


parallel_chain = RunnableParallel({
    'content': itemgetter('query') | retriever | RunnableLambda(format_docs),
    'query': itemgetter('query')
})