from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(
        text:str,
        # chunk_size:int = 1000  Each chunk can contain upto 1000 characters we don't use this because it cuts words arbitrarily
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    
    chunks =splitter.split_text(text)

    return chunks
