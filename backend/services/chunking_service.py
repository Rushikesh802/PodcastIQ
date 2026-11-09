from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunking(transcipt: list):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=120
    )

    return splitter.create_documents(texts=[transcipt])


