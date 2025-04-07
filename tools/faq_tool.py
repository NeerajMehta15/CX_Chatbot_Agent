from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
import utils.config as config


def load_documents(faq_path: str):
    """Load documents from the FAQ CSV file."""
    loader = CSVLoader(file_path=faq_path, source_column="question")
    return loader.load()


def split_into_chunks(data, chunk_size=150, chunk_overlap=2):
    """Split documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    all_chunks = []
    for doc in data:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            all_chunks.append(doc.__class__(page_content=chunk, metadata=doc.metadata))
    return all_chunks


def create_vector_store(chunks):
    """Create a vector store from a list of text chunks using Mistral embeddings."""
    embeddings_model = MistralAIEmbeddings(model="mistral-embed")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=config.VECTOR_STORE_PATH
    )
    return vector_store


def get_faq_answer(user_query: str, vector_store, config) -> str:
    """Retrieve an answer from the FAQ vector store based on the user query."""
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": config.TOP_K}
    )
    relevant_docs = retriever.get_relevant_documents(user_query)
    if relevant_docs:
        return relevant_docs[0].page_content
    else:
        return "I couldn't find an answer to your question in our FAQ database."


def initialize_vector_store():
    """Initialize vector store from the FAQ data."""
    documents = load_documents(config.FAQ_PATH)
    chunks = split_into_chunks(documents)
    vector_store = create_vector_store(chunks)
    return vector_store
