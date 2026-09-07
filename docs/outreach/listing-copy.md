# Canonical listing copy (2026-08-30)

Use verbatim in every directory. Source of truth for wording.

**One-liner:** Extract, search and tag any document — invoices, receipts, contracts, forms, or your own templates. 14 tools, one sign-in, free FileTag tier, data residency in the EU, US, Israel or Asia.

**Registry description (≤100):** Extract, search and tag any document: invoices, receipts, contracts, templates. OAuth or API key.

**Long description:**

Gemina is a hosted MCP server for working with documents of any kind — invoices, receipts, contracts, forms, statements, delivery notes, or any other PDF or image your team handles. Define your own custom templates to extract exactly the fields you need from any document type. One endpoint, 14 tools in three groups.

• FileTag (free tier, 1,500 tags/month, no credit card): turn any PDF or image into structured metadata, six suggested filenames, and a metadata-embedded copy. Upload a file (files_create_upload → tag_file) or point at a public URL (tag_url).

• Extraction: OCR for any document, custom templates for your own document types and fields, plus ready-made invoice headers, invoice line items, and Hebrew document details and line items (extract_document, get_extraction_result, list_extractions, get_extraction, get_document, add_document_extractions, submit_extraction_feedback).

• Document Intelligence: ask questions and run spend analytics across your whole indexed collection, no re-upload — search with structured, semantic or hybrid queries (query_documents) and run sums, averages and counts grouped by vendor, currency, type or month, e.g. “total spent per vendor last quarter” (aggregate_documents). Documents you tag or run a structured extraction on are submitted for indexing automatically when indexing is enabled — plain OCR is excluded and some documents can be skipped, e.g. no extractable fields or no indexing credits (index_document to (re)index on demand).

Sign in with your Gemina account — no keys to paste. The free tier covers FileTag; Extraction and Document Intelligence need a paid plan. Supports PDF, PNG, JPEG, GIF, WebP, HEIC/HEIF and AVIF up to 50 MB. You choose the data-center region per account (EU, US, Israel or Asia), so documents are stored and processed where you decide.
