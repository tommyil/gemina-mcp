"""GeminaFileTagReader — a LlamaIndex reader that tags every document with FileTag.

Each loaded Document carries the structured metadata from FileTag — vendor, date,
document_type, amount, etc. — so retrieval can pre-filter by metadata before
running the semantic search.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests
from llama_index.core import Document
from llama_index.core.readers.base import BaseReader

TAG_ENDPOINT = "https://api.gemina.co/api/v1/filetag"
SUPPORTED_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


class GeminaFileTagReader(BaseReader):
    """Read documents from a directory and enrich each with FileTag metadata.

    Args:
        api_key: Gemina API key. Falls back to ``GEMINA_API_KEY`` env var.
        timeout: Per-request timeout in seconds. Default: 120.

    Returns LlamaIndex Document objects whose ``metadata`` includes:
        document_type, vendor, date, amount, currency, document_number, tags,
        filename, filetag_document_id.
    """

    def __init__(self, api_key: Optional[str] = None, timeout: float = 120.0) -> None:
        super().__init__()
        self.api_key = api_key or os.environ.get("GEMINA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINA_API_KEY is required (pass via api_key= or set env var)"
            )
        self.timeout = timeout

    def load_data(self, input_dir: str | Path, **_) -> list[Document]:
        root = Path(input_dir)
        if not root.is_dir():
            raise ValueError(f"{input_dir} is not a directory")

        docs: list[Document] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTS:
                continue
            doc = self._load_one(path)
            if doc is not None:
                docs.append(doc)
        return docs

    def _load_one(self, path: Path) -> Optional[Document]:
        with path.open("rb") as f:
            response = requests.post(
                TAG_ENDPOINT,
                headers={"X-API-Key": self.api_key},
                files={"file": (path.name, f)},
                timeout=self.timeout,
            )
        response.raise_for_status()
        result = response.json()

        metadata = dict(result.get("metadata") or {})
        metadata["filename"] = path.name
        metadata["filetag_document_id"] = result.get("document_id")

        text = self._derive_text(metadata, path)
        return Document(text=text, metadata=metadata)

    @staticmethod
    def _derive_text(metadata: dict, path: Path) -> str:
        """Generate a human-readable text body from the metadata.

        For most use cases you'll want to layer this on top of a real OCR/parser
        pipeline (e.g., PyMuPDF, pdfplumber, the Gemina extraction API for full
        line-item extraction). This stub keeps the example self-contained.
        """
        lines = [f"Document: {path.name}"]
        for key in ("document_type", "vendor", "date", "amount", "currency", "document_number"):
            if metadata.get(key) is not None:
                lines.append(f"{key}: {metadata[key]}")
        if metadata.get("tags"):
            lines.append(f"tags: {', '.join(metadata['tags'])}")
        return "\n".join(lines)
