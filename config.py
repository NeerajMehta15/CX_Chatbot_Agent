from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

# API keys
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding & vector store settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./data/chroma")

# Retrieval settings
TOP_K = int(os.getenv("TOP_K", 3))

# LLM parameters
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))
MAX_LENGTH = int(os.getenv("MAX_LENGTH", 512))
TOP_P = float(os.getenv("TOP_P", 0.95))

# File paths
FAQ_PATH = os.getenv("FAQ_PATH", "./data/faq.csv")
