from langchain_core.runnables import RunnableParallel, RunnablePassthrough,  RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from backend.services.vector_service import vectore_store


def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text


def get_context(query):
    retriver = vectore_store.as_retriever(search_kwargs={'k': 4})

    parallel_chain = RunnableParallel({
    'content': retriver | RunnableLambda(format_docs),
    'query': RunnablePassthrough()
    })

    return parallel_chain.invoke(query)

r = vectore_store.similarity_search('hi')

print(r)

