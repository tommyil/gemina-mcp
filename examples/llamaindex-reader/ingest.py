"""Demo: load a folder with GeminaFileTagReader and print the resulting Documents."""

from __future__ import annotations

import sys
from pathlib import Path

from gemina_reader import GeminaFileTagReader


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <input_dir>", file=sys.stderr)
        return 2

    reader = GeminaFileTagReader()
    documents = reader.load_data(input_dir=Path(sys.argv[1]))

    print(f"Loaded {len(documents)} document(s).\n")
    for doc in documents:
        print(f"--- {doc.metadata.get('filename')} ---")
        for key, value in doc.metadata.items():
            print(f"  {key}: {value}")
        print(doc.text)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
