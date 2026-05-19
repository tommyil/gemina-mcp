# bulk-tag-folder

Walk a local directory, tag every supported file with Gemina FileTag, and write the results to disk. Handy for filing a backlog of receipts, invoices, contracts, or scans.

## What it does

For every PDF/PNG/JPEG/GIF/WebP in the input directory (recursive):

1. Uploads to FileTag's REST endpoint.
2. Writes the JSON response to `output/<original-filename>.json`.
3. Downloads the enriched copy (PDF metadata or EXIF embedded) under the API's suggested filename into `output/enriched/`.
4. Prints a one-line summary per file.

Skips files that have already been tagged (idempotent on re-run — based on the existence of the JSON output).

## Setup

```bash
cd examples/bulk-tag-folder
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GEMINA_API_KEY="paste-your-key-here"
```

## Run

```bash
python bulk_tag.py /path/to/your/documents

# Or, with a custom output directory:
python bulk_tag.py /path/to/your/documents --output /path/to/results

# Dry-run (lists files that would be tagged, makes no API calls):
python bulk_tag.py /path/to/your/documents --dry-run
```

## Output layout

```
output/
├── invoice_2024_acme.pdf.json        ← FileTag response
├── invoice_2024_acme.pdf.error.txt   ← (only if the call failed)
└── enriched/
    └── 2024-03-15_Acme-Corp_Invoice.pdf   ← downloaded enriched copy
```

## Rate limits

The free tier allows ~10 calls per second and 1,500 calls per month. `bulk_tag.py` paces requests at ~5/sec by default to leave headroom — adjust with `--rate-limit`.

## What's next

- Pipe the JSON outputs into a database for filtering and search.
- Move files into per-vendor or per-type folders based on the metadata.
- Switch to async with `httpx + asyncio` for higher throughput on paid plans.
