from backend.schemas.chat import augmentation_prompt, query_checker
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from backend.schemas.query_validator import Query
from langchain_core.runnables import RunnableBranch, RunnableLambda
from backend.services.vector_service import get_full_content
from backend.services.retrieval_service import get_retrieval_chain
from langchain_classic.chains.summarize import load_summarize_chain
from backend.services.summarization_service import summarize_video


## Parser for output
py_parser = PydanticOutputParser(pydantic_object=Query)
str_parser = StrOutputParser()

# intent of user checking chain
intent_chain = query_checker | chat_model | py_parser 


summarize_runnable_lambda= RunnableLambda(summarize_video)

# important default rag chain
def genrate_rag_answer(inputs: dict):

    rag_chain = get_retrieval_chain(video_id=inputs['video_id']) | augmentation_prompt | chat_model | str_parser

    return rag_chain.invoke({'query': inputs['query']})

rag_runnable = RunnableLambda(genrate_rag_answer)

#conditional execution
main_chain = RunnableBranch(
         (lambda x:x['intent'] == 'summarize', summarize_runnable_lambda),

         #default chain
         rag_runnable
    )

def final_output(user_query: str, video_id: str):

    intent_result = intent_chain.invoke({'query': user_query})

    return main_chain.invoke({
         'query': user_query,
         'intent': intent_result.query,
         'video_id': video_id
         })
