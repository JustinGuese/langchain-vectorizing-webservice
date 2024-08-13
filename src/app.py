from typing import List

from fastapi import FastAPI
from langchain_core.documents import Document
from pydantic import BaseModel

from vectorstore import getVectorstore

app = FastAPI(title="Langchain Vectorizing API")


class LangChainDocument(BaseModel):
    id: None
    metadata: dict = {}
    type: str = "Document"
    page_content: str


@app.post("/{namespace}")
def ingestDocument(document: LangChainDocument, namespace: str = "default"):
    if namespace is None:
        namespace = "default"
    document = Document(
        metadata=document.metadata,
        type=document.type,
        page_content=document.page_content,
    )
    vectorstore = getVectorstore(namespace)
    vectorstore.add_documents([document])
    return {"status": "ok"}


@app.get("/search/{namespace}", response_model=List[LangChainDocument])
def searchVectorstore(query: str, namespace: str = "default"):
    if namespace is None:
        namespace = "default"
    vectorstore = getVectorstore(namespace)
    results = vectorstore.similarity_search(query, k=10)
    results = [LangChainDocument(**result.dict()) for result in results]
    for r in results:
        if r.id is None:
            r.id = r.metadata.get("id", None)
    return results
