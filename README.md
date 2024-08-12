a python web app / api allowing ingestion of langchain documents into a vector database

## why?

the embedder takes quite some space in the docker image, i rather want to have a seperate service for it

## usage?

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
req = requests.post("http://localhost:8000/", json=doc.dict())
req.raise_for_status()
```
## install:

### docker

 guestros/langchain-vectorizer-webservice:latest

 see docker-compose.yml or `docker compose up`
 
### local

```
poetry install
poetry run uvicorn src/app:app --reload
```