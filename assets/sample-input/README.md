# Sample input documents

Fully synthetic PDFs used by the [examples](../../examples). All names, addresses, amounts, and identifiers are fictitious — safe to use in any public context.

| File | Type | Pages | What it covers |
|---|---|---|---|
| [`invoice.pdf`](./invoice.pdf) | Vendor invoice | 1 | Header (invoice #, dates, vendor, bill-to, payment terms, tax ID) + 6-line item table + tax + totals |
| [`receipt.pdf`](./receipt.pdf) | Retail receipt | 1 | Narrow café receipt — merchant, date, items, subtotal, tax, total, payment method |
| [`contract.pdf`](./contract.pdf) | Master Services Agreement | 3 | Multi-page contract with parties, term, fees, SLA, confidentiality, liability, signatures |

## Running the examples against these files

```bash
# From the repo root:
export GEMINA_API_KEY="paste-your-key-here"

# Tag every sample with curl:
for f in assets/sample-input/*.pdf; do
  curl -sX POST https://api.gemina.co/api/v1/filetag \
    -H "X-API-Key: ${GEMINA_API_KEY}" \
    -F "file=@${f}" | jq .
done

# Or bulk-tag with the Python example:
cd examples/bulk-tag-folder
pip install -r requirements.txt
python bulk_tag.py ../../assets/sample-input
```

## Regenerating the PDFs

The PDFs are produced by [`_generate.py`](./_generate.py) using [ReportLab](https://www.reportlab.com/). Edit the script to change companies, line items, dates, or layout, then:

```bash
pip install reportlab
python assets/sample-input/_generate.py
```

The script overwrites the existing PDFs in place.

## Notes for maintainers

- Keep everything in this directory **non-confidential** — synthetic only. No real vendor names, no PII.
- The corresponding FileTag JSON responses (when refreshed) live in [`../sample-output/`](../sample-output).
- Don't add huge files here. Keep each PDF under ~50 KB so cloning the repo stays fast.
