from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunking(transcipt):

    docs = [Document(page_content=transcipt, metadata={})]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )

    return splitter.split_documents(documents=docs)

