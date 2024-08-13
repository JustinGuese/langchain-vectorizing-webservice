from os import environ

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name=environ.get("EMBEDDING_HF_MODEL", "dunzhang/stella_en_1.5B_v5")
)
