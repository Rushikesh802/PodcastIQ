from backend.schemas.chat import prompt
from backend.model.all import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
from backend.services.retrieval_service import parallel_chain

parser = StrOutputParser()


def final_output(query):

    summarize = 


    chain = parallel_chain | prompt | chat_model | parser
    
    return chain.invoke(query) 

def summarize_video():
    pass


