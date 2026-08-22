from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(
    text: str,
):
    # Use LangChain's RecursiveCharacterTextSplitter because it intelligently splits large text into smaller chunks while
    # preserving context. Unlike fixed-size splitting, it tries to break text at natural boundaries such as paragraphs,
    # sentences, and spaces before falling back to character limits. This produces more meaningful chunks for embedding 
    # generation and improves retrieval quality in a RAG system.
    splitter = RecursiveCharacterTextSplitter(
        # Maximum number of characters per chunk
        chunk_size=1000,

        # Number of characters shared between consecutive chunks
        # to maintain context across chunk boundaries
        chunk_overlap=200,
    )

    # Split the extracted text into chunks
    chunks = splitter.split_text(text)

    return chunks