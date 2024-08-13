from os import environ

from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

from embedder import embeddings

# See docker command above to launch a postgres instance with pgvector enabled.
connection = "postgresql+psycopg://" + environ["PGVECTOR_URI"]  # Uses psycopg3!

VECTORSTORES = dict()


def getVectorstore(collection_name: str) -> PGVector:
    if collection_name not in VECTORSTORES:
        VECTORSTORES[collection_name] = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=connection,
            use_jsonb=True,
        )
    return VECTORSTORES[collection_name]
