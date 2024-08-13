a python web app / api allowing ingestion of langchain documents into a vector database

## why?

the embedder takes quite some space in the docker image, i rather want to have a seperate service for it

## usage?

Check Swagger at [http://localhost:8000/docs](http://localhost:8000/docs) or [openapi.json](openapi.json)

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

### querying the vector database (similarity search)

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

### questioning the database with an llm

OPENAI_API_KEY needs to be set in the environment

```bash
curl -X 'GET' \
  'http://localhost:8000/document-chat/tb24_news?question=what%27s%20microsoft%20up%20to%3F' \
  -H 'accept: application/json'
```

Response:

```json
{
  "question": "what's microsoft up to?",
  "answer": "I don't know. The provided context doesn't mention Microsoft. It appears to be about a securities class action related to Direct Digital Holdings, Inc. (DRCT).",
  "source_documents": [
    {
      "id": null,
      "metadata": {
        "id": 954,
        "url": "https://www.benzinga.com/pressreleases/24/07/g39851872/drct-deadline-rosen-leading-investor-counsel-encourages-direct-digital-holdings-inc-investors-to-s",
        "title": "DRCT DEADLINE: ROSEN, LEADING INVESTOR COUNSEL, Encourages Direct Digital Holdings, Inc. Investors to Secure Counsel Before Important July 22 Deadline in Securities Class Action - DRCT - Direct Digital Holdings  ( NASDAQ:DRCT ) ",
        "author": "Globe Newswire",
        "source": "Benzinga",
        "tickers": ["DRCT"],
        "category": "News",
        "timestamp": "2024-07-18 23:56:00"
      },
      "type": "Document",
      "page_content": "DRCT DEADLINE: ROSEN, LEADING INVESTOR COUNSEL, Encourages Direct Digital Holdings, Inc. Investors to Secure Counsel Before Important July 22 Deadline in Securities Class Action - DRCT - Direct Digital Holdings  ( NASDAQ:DRCT )  NEW YORK, July 18, 2024 ( GLOBE NEWSWIRE ) -- WHY: Rosen Law Firm, a global investor rights law firm, reminds purchasers of common stock of Direct Digital Holdings, Inc. DRCT between April 17, 2023 and March 25, 2024, both dates inclusive ( the \"Class Period\" ) of the important July 22, 2024 lead ..."
    }
  ],
  "chat_history": [
    {
      "human": true,
      "content": "what's microsoft up to?"
    },
    {
      "human": false,
      "content": "I don't know. The provided context doesn't mention Microsoft. It appears to be about a securities class action related to Direct Digital Holdings, Inc. (DRCT)."
    }
  ]
}
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