from backend.schemas.chat import augmentation_prompt, query_checker
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from backend.schemas.query_validator import Query
from langchain_core.runnables import RunnableBranch, RunnableLambda
from backend.services.vector_service import get_full_content
from backend.services.retrieval_service import parallel_chain
from langchain_classic.chains.summarize import load_summarize_chain
from backend.services.cache_service import get_cached_summary, cache_summary


## Parser for output
py_parser = PydanticOutputParser(pydantic_object=Query)
str_parser = StrOutputParser()

# intent of user checking chain
intent_chain = query_checker | chat_model | py_parser 
summarize_chain = load_summarize_chain(
    llm=chat_model,
    chain_type='map_reduce',
    verbose=False
    )


def summarize_video(inputs: dict):
     video_id = ['video_id']
     #check redis cache
     cached_summary = get_cached_summary(video_id)

     if cached_summary:
        print('summary cache HIT')
        return cached_summary
     print('summary cache MISS')

     # Retrive documents from vector store
     content = get_full_content()

     # Genrate summary
     result = summarize_chain.invoke({'input_documents': content})
     summary =result['output_text']
     cache_summary(video_id=video_id, summary=summary)
     return summary

summarize_runnable_lambda= RunnableLambda(summarize_video)

# important default rag chain
rag_chain = parallel_chain | augmentation_prompt | chat_model | str_parser

main_chain = RunnableBranch(
         (lambda x:x['intent'] == 'summarize', summarize_runnable_lambda),

         #default chain
         rag_chain
    )

def final_output(user_query: str, video_id: str):

    intent_result = intent_chain.invoke({'query': user_query})

    return main_chain.invoke({
         'query': user_query,
         'intent': intent_result.query,
         'video_id': video_id
         })
