FROM python:3.11-slim
RUN pip install poetry 
WORKDIR /app
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY ./src/ /app/
# download embedder model
RUN python embedder.py
CMD ["uvicorn", "app:app.py", "--host", "0.0.0.0"]