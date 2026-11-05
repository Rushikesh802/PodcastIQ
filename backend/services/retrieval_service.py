from langchain_core.runnables import RunnableParallel, RunnablePassthrough,  RunnableLambda
from backend.services.vector_service import get_vector_store


def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text



retriver = get_vector_store().as_retriever(search_kwargs={'k': 4})



parallel_chain = RunnableParallel({
    'content': retriver | RunnableLambda(format_docs),
    'query': RunnablePassthrough()
})
