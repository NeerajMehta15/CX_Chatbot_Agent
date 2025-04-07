from setuptools import setup, find_packages

setup(
    name="cx_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-community",
        "langchainhub",
        "chromadb",
        "pandas",
        "python-dotenv",
        "groq"
    ],
)
