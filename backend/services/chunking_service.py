from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunking(document: Document) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        add_start_index=True
    )

    return splitter.split_documents([document])
