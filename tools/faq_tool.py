from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import config


def load_documents(faq_path: str):
    """Load documents from the FAQ CSV file."""
    loader = CSVLoader(file_path=faq_path, source_column="question")
    faqs = loader.load()
    return faqs


def split_into_chunks(data, chunk_size=150, chunk_overlap=2):
    """
    Split documents into smaller chunks.
    
    Args:
        data (list): List of Document objects with page_content to process.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Overlap between chunks.
    
    Returns:
        list: List of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""],chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    all_chunks = []
    for doc in data:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            all_chunks.append(doc.__class__(page_content=chunk, metadata=doc.metadata))
    return all_chunks


def create_vector_store(chunks, config):
    """
    Create a vector store from a list of text chunks using HuggingFace embeddings.
    
    Args:
        chunks (list): Text chunks from the FAQ data.
        config: Configuration object with embedding and persistence settings.
    
    Returns:
        vector_store: A Chroma vector store object.
    """
    embeddings_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL,model_kwargs={'device': 'cpu'})
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=config.VECTOR_STORE_PATH
    )
    return vector_store


def get_faq_answer(user_query: str, vector_store, config) -> str:
    """
    Retrieve an answer from the FAQ vector store based on the user query.
    
    Args:
        user_query (str): The user's question.
        vector_store: The Chroma vector store object.
        config: Configuration object with retrieval settings.
    
    Returns:
        str: The best-matched answer or a fallback message.
    """
    retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k": config.TOP_K})
    relevant_docs = retriever.get_relevant_documents(user_query)
    if relevant_docs:
        return relevant_docs[0].page_content
    else:
        return "I couldn't find an answer to your question in our FAQ database."