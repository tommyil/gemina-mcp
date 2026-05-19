# llamaindex-reader

A custom LlamaIndex reader that wraps each document with Gemina FileTag metadata before it lands in your index. Lets you filter retrieval by vendor, date, document type, and other structured fields — much faster and more accurate than re-extracting that metadata at query time.

## Why this matters for RAG

Vanilla document ingestion treats every PDF as a bag of text. When a user asks "what did we pay Acme Corp last quarter?", the retriever ranks chunks by semantic similarity to the question — which is brittle, because the answer chunk may not mention "Acme" or "paid" verbatim.

FileTag fixes this by attaching `metadata.vendor = "Acme Corp"` and `metadata.date = "2025-11-12"` to every chunk at ingestion time. Now retrieval can pre-filter to vendor=Acme + date in Q4 before running the semantic search. Cheaper, faster, more accurate.

## Setup

```bash
cd examples/llamaindex-reader
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINA_API_KEY="paste-your-key-here"
```

## Run

```bash
python ingest.py /path/to/documents
```

This loads every supported file under the path, tags it with FileTag, and prints the resulting LlamaIndex `Document` objects with their metadata. Plug `GeminaFileTagReader` into your own ingestion pipeline:

```python
from gemina_reader import GeminaFileTagReader
from llama_index.core import VectorStoreIndex

reader = GeminaFileTagReader(api_key=os.environ["GEMINA_API_KEY"])
documents = reader.load_data(input_dir="/path/to/documents")
index = VectorStoreIndex.from_documents(documents)
```

Each `Document.metadata` now contains:

```python
{
    "document_type": "invoice",
    "vendor": "Acme Corp",
    "date": "2026-02-15",
    "amount": 7200,
    "currency": "ILS",
    "document_number": "12345",
    "tags": ["vendor", "invoice"],
    "filename": "invoice.pdf",
    "filetag_document_id": "abc-123"
}
```

## Filtered retrieval

```python
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters

filters = MetadataFilters(
    filters=[
        MetadataFilter(key="vendor", value="Acme Corp"),
        MetadataFilter(key="document_type", value="invoice"),
    ]
)
retriever = index.as_retriever(filters=filters)
nodes = retriever.retrieve("what did we pay last quarter?")
```

## What's next

- Persist the FileTag JSON alongside the index for re-indexing without re-tagging.
- Use the `enriched_file_url` to store a copy with metadata baked into the PDF — useful for downstream tools that read PDF properties directly.
- See the equivalent for LangChain: [langchain-loader](../langchain-loader).
