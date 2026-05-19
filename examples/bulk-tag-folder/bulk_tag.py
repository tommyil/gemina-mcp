"""Bulk-tag every supported document in a folder with Gemina FileTag.

Usage:
    python bulk_tag.py <input_dir> [--output <dir>] [--rate-limit <calls/sec>] [--dry-run]

Requires:
    GEMINA_API_KEY environment variable. Get a free key at
    https://console.gemina.co/registration/create-account
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://api.gemina.co"
TAG_ENDPOINT = f"{API_BASE}/api/v1/filetag"
SUPPORTED_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


def iter_documents(root: Path) -> list[Path]:
    """Return every supported file under root, sorted for deterministic ordering."""
    return sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS
    )


def tag_file(path: Path, api_key: str) -> dict:
    """POST a file to FileTag and return the parsed JSON response."""
    with path.open("rb") as f:
        response = requests.post(
            TAG_ENDPOINT,
            headers={"X-API-Key": api_key},
            files={"file": (path.name, f)},
            timeout=120,
        )
    response.raise_for_status()
    return response.json()


def download_enriched(url: str, target: Path) -> None:
    """Stream the enriched-file URL to disk."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with target.open("wb") as f:
            for chunk in response.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory to scan recursively.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Where to write JSON responses and enriched files. Default: ./output",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=5.0,
        help="Max calls per second. Default: 5 (free-tier safe).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be tagged but make no API calls.",
    )
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"error: {args.input_dir} is not a directory", file=sys.stderr)
        return 2

    api_key = os.environ.get("GEMINA_API_KEY")
    if not api_key and not args.dry_run:
        print(
            "error: set GEMINA_API_KEY (get a free key at "
            "https://console.gemina.co/registration/create-account)",
            file=sys.stderr,
        )
        return 2

    documents = iter_documents(args.input_dir)
    if not documents:
        print(f"No supported files found under {args.input_dir}")
        return 0

    print(f"Found {len(documents)} document(s) to tag.")
    if args.dry_run:
        for p in documents:
            print(f"  [dry-run] {p}")
        return 0

    args.output.mkdir(parents=True, exist_ok=True)
    delay = 1.0 / args.rate_limit if args.rate_limit > 0 else 0
    tagged = skipped = failed = 0

    for path in documents:
        json_target = args.output / f"{path.name}.json"
        if json_target.exists():
            print(f"  skip   {path.name} (already tagged)")
            skipped += 1
            continue

        try:
            result = tag_file(path, api_key)
        except requests.HTTPError as e:
            failed += 1
            err_target = args.output / f"{path.name}.error.txt"
            err_target.write_text(f"{e}\n{getattr(e.response, 'text', '')}\n")
            print(f"  FAIL   {path.name}: {e}", file=sys.stderr)
            continue

        json_target.write_text(json.dumps(result, indent=2, ensure_ascii=False))

        enriched_url = result.get("enriched_file_url")
        suggested = result.get("suggested_filename") or path.name
        if enriched_url:
            try:
                download_enriched(enriched_url, args.output / "enriched" / suggested)
            except requests.HTTPError as e:
                print(
                    f"  warn   {path.name}: enriched download failed: {e}",
                    file=sys.stderr,
                )

        tagged += 1
        print(f"  ok     {path.name} → {suggested}")

        if delay:
            time.sleep(delay)

    print(f"\nDone. tagged={tagged} skipped={skipped} failed={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
