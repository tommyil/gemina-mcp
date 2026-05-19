# langchain-loader

A LangChain `BaseLoader` that enriches each loaded document with Gemina FileTag metadata. The LangChain equivalent of [llamaindex-reader](../llamaindex-reader).

## Why FileTag at ingestion time?

Same argument as the LlamaIndex example: filtering retrieval by structured metadata (vendor, date, document type) is orders of magnitude more accurate than asking the LLM to figure it out from raw chunks. FileTag is the cheapest way to get that metadata at ingestion.

## Setup

```bash
cd examples/langchain-loader
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINA_API_KEY="paste-your-key-here"
```

## Run

```bash
python ingest.py /path/to/documents
```

Or integrate `GeminaFileTagLoader` into your own pipeline:

```python
from gemina_loader import GeminaFileTagLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

loader = GeminaFileTagLoader(directory="/path/to/documents")
documents = loader.load()
db = Chroma.from_documents(documents, OpenAIEmbeddings())
```

Each `Document.metadata` carries the FileTag structured fields, so you can run filtered retrieval:

```python
results = db.similarity_search(
    "what did we pay Acme last quarter?",
    k=4,
    filter={"vendor": "Acme Corp"},
)
```

## What's next

- See the LlamaIndex equivalent: [llamaindex-reader](../llamaindex-reader)
- For full text extraction (not just metadata), combine this loader with `PyPDFLoader` or `UnstructuredFileLoader` and merge the metadata.
