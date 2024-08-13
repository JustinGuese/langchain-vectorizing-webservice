from enum import Enum
from os import environ
from typing import List

from fastapi import FastAPI, HTTPException
from langchain.chains import ConversationalRetrievalChain
from langchain_core.documents import Document
from langchain_core.messages.human import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from memory import getMemory
from vectorstore import getVectorstore

app = FastAPI(title="Langchain Vectorizing API")

if environ.get("OPENAI_API_KEY") is not None:
    llm = ChatOpenAI(
        api_key=environ.get("OPENAI_API_KEY"),
        base_url=environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=environ.get("OPENAI_MODEL", "gpt-4o"),
    )
else:
    llm = None


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


class ChatMessage(BaseModel):
    human: bool = False
    content: str


class DocumentChatResponse(BaseModel):
    question: str
    answer: str
    source_documents: List[LangChainDocument]
    chat_history: List[ChatMessage]


def response2Pydantic(response: dict) -> DocumentChatResponse:
    chathistory = []
    for m in response["chat_history"]:
        m = ChatMessage(content=m.content)
        if isinstance(m, HumanMessage):
            m.human = True
        chathistory.append(m)

    return DocumentChatResponse(
        question=response["question"],
        answer=response["answer"],
        source_documents=[
            LangChainDocument(**doc.dict()) for doc in response["source_documents"]
        ],
        chat_history=chathistory,
    )


@app.get("/document-chat/{namespace}", response_model=DocumentChatResponse)
def getAIChatResponse(question: str, namespace: str = "default"):
    global llm
    if llm is None:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not set. Set the OPENAI_API_KEY environment variable to use ai-chat feature.",
        )
    if namespace is None:
        namespace = "default"
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=getVectorstore(namespace).as_retriever(),
        return_source_documents=True,
        memory=getMemory(namespace),
    )
    results = chain.invoke({"question": question})
    results = response2Pydantic(results)
    return results
