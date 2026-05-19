"""GeminaFileTagLoader — a LangChain document loader that adds FileTag metadata.

Each yielded Document carries FileTag's structured fields (vendor, date,
document_type, amount, etc.) so retrieval can filter by metadata.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator, Optional

import requests
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

TAG_ENDPOINT = "https://api.gemina.co/api/v1/filetag"
SUPPORTED_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


class GeminaFileTagLoader(BaseLoader):
    """Load files from a directory and enrich each Document with FileTag metadata.

    Args:
        directory: Path to scan recursively.
        api_key: Gemina API key. Falls back to ``GEMINA_API_KEY`` env var.
        timeout: Per-request timeout in seconds. Default: 120.
    """

    def __init__(
        self,
        directory: str | Path,
        api_key: Optional[str] = None,
        timeout: float = 120.0,
    ) -> None:
        self.directory = Path(directory)
        if not self.directory.is_dir():
            raise ValueError(f"{directory} is not a directory")
        self.api_key = api_key or os.environ.get("GEMINA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINA_API_KEY is required (pass via api_key= or set env var)"
            )
        self.timeout = timeout

    def lazy_load(self) -> Iterator[Document]:
        for path in sorted(self.directory.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTS:
                continue
            yield self._tag(path)

    def _tag(self, path: Path) -> Document:
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
        metadata["source"] = str(path)
        metadata["filename"] = path.name
        metadata["filetag_document_id"] = result.get("document_id")

        lines = [f"Document: {path.name}"]
        for key in ("document_type", "vendor", "date", "amount", "currency", "document_number"):
            if metadata.get(key) is not None:
                lines.append(f"{key}: {metadata[key]}")
        if metadata.get("tags"):
            lines.append(f"tags: {', '.join(metadata['tags'])}")

        return Document(page_content="\n".join(lines), metadata=metadata)
