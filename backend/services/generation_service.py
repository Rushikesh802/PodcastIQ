from backend.schemas.chat import augmentation_prompt, summarize_prompt, query_checker
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from backend.schemas.query_validator import Query
from langchain_core.runnables import RunnableBranch
from backend.services.vector_service import get_full_content
from backend.services.retrieval_service import parallel_chain


## Parser for output
py_parser = PydanticOutputParser(pydantic_object=Query)
parser = StrOutputParser()

# intent of user checking chain
intent = query_checker | chat_model | py_parser 

chain = parallel_chain | augmentation_prompt | chat_model | parser


def summarize_video():
     content = get_full_content()
     summarize = summarize_prompt | chat_model | parser
     return summarize.invoke({'content': content})

def final_output(user_query: str):


    intent_result = intent.invoke({'query': user_query}).query

    if intent_result == 'summarize':
         return summarize_video()

    return chain.invoke({'query': user_query})
