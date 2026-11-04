from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunking(transcipt):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )

    return splitter.create_documents([transcipt])


