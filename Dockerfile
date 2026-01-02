FROM python:3.13-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir \
    python-dotenv \
    qdrant-client==1.15 \
    requests \
    fastapi \
    uvicorn \
    pandas \
    ollama \
    pymupdf \
    pdfplumber \
    httpx \
    langchain \
    langchain-text-splitters \
    aiohttp \
    langchain-community \
    langchain-ollama \
    langchain-core \
    pydantic-settings \
    pytz \
    "psycopg[binary]" \
    langchain-postgres \
    asyncpg \
    python-multipart \
    langchain-qdrant

EXPOSE 9534

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9534", "--workers", "3" ]