a python web app / api allowing ingestion of langchain documents into a vector database

## why?

the embedder takes quite some space in the docker image, i rather want to have a seperate service for it

## usage?

### adding a document to the vector database

from your service that creates the langchain document:

```python
from langchain_core.documents import Document
import requests

doc = Document(
    page_content=article.title + " " + article.summary,
    metadata=dict(
        id=article.id,
        timestamp=article.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        author=article.author,
        title=article.title,
    ),
)
req = requests.post("http://localhost:8000/[NAMESPACE]", json=doc.dict())
req.raise_for_status()
```

where NAMESPACE is "default" if nothing it set, otherwise you can set it as URL param

### querying the vector database

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search/tb24_news?query=oil%20microsoft' \
  -H 'accept: application/json'
```

```python
import requests
js = {"query": "Microsoft and OIL investments"}
req = requests.get("http://localhost:8000/tb24_news", json=js)
req.raise_for_status()
```

## install:

### docker

 guestros/langchain-vectorizer-webservice:latest

 see docker-compose.yml or `docker compose up`
 
### local

```
poetry install
docker compose up pgvector
poetry run uvicorn src/app:app --reload
```