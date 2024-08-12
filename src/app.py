from fastapi import FastAPI
from langchain_core.documents import Document
from pydantic import BaseModel

from vectorstore import vectorstore

app = FastAPI()


class LangChainDocument(BaseModel):
    id: None
    metadata: dict = {}
    type: str = "Document"
    page_content: str


@app.post("/")
def ingestDocument(document: LangChainDocument):
    document = Document(
        metadata=document.metadata,
        type=document.type,
        page_content=document.page_content,
    )
    vectorstore.add_documents([document])
    return {"status": "ok"}
