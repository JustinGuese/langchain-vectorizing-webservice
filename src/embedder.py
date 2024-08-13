from os import environ

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name=environ.get("EMBEDDING_HF_MODEL", "all-MiniLM-L6-v2")
)
