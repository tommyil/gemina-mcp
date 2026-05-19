"""Demo: load a folder with GeminaFileTagLoader and print the resulting Documents."""

from __future__ import annotations

import sys

from gemina_loader import GeminaFileTagLoader


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <input_dir>", file=sys.stderr)
        return 2

    loader = GeminaFileTagLoader(directory=sys.argv[1])
    documents = list(loader.lazy_load())

    print(f"Loaded {len(documents)} document(s).\n")
    for doc in documents:
        print(f"--- {doc.metadata.get('filename')} ---")
        for key, value in doc.metadata.items():
            print(f"  {key}: {value}")
        print(doc.page_content)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
