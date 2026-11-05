from backend.schemas.chat import augmentation_prompt, summarize_prompt, query_checker
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from backend.schemas.query_validator import Query
from langchain_core.runnables import RunnableBranch, RunnableLambda
from backend.services.vector_service import get_full_content
from backend.services.retrieval_service import parallel_chain


## Parser for output
py_parser = PydanticOutputParser(pydantic_object=Query)
str_parser = StrOutputParser()

# intent of user checking chain
intent_chain = query_checker | chat_model | py_parser 

def summarize_video(inputs: dict):
     content = get_full_content()
     summarize_chain = summarize_prompt | chat_model | str_parser
     return summarize_chain.invoke({'content': content})

summarize_chain = RunnableLambda(summarize_video())

# important default rag chain
rag_chain = parallel_chain | augmentation_prompt | chat_model | str_parser

main_chain = RunnableBranch(
         (lambda x:x['intent'] == 'summarize', summarize_chain),

         #default chain
         rag_chain
    )

def final_output(user_query: str):

    intent_result = intent_chain.invoke({'query': user_query})

    return main_chain.invoke({
         'query': user_query,
         'intent': intent_result.query
         })
