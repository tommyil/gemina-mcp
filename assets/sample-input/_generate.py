"""Generate the synthetic sample PDFs used by the examples.

Run from this directory:
    python _generate.py

Produces:
    invoice.pdf   — vendor invoice with header + line items
    receipt.pdf   — retail receipt
    contract.pdf  — simple service agreement (multi-page)

All data is fully synthetic — fake companies, fake addresses, fake amounts.
Safe to use in any public example.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

HERE = Path(__file__).parent


def styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1d4ed8"),
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#1e3a8a"),
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontSize=10,
            leading=14,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontSize=8,
            leading=11,
            textColor=colors.grey,
        ),
    }


def invoice() -> None:
    s = styles()
    doc = SimpleDocTemplate(
        str(HERE / "invoice.pdf"),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Invoice #INV-2026-00148",
        author="Acme Office Supplies Ltd.",
    )

    story: list = []
    story.append(Paragraph("INVOICE", s["title"]))
    story.append(Paragraph("Acme Office Supplies Ltd.", s["body"]))
    story.append(
        Paragraph(
            "742 Synthetic Avenue, Springfield, IL 62701 · billing@acme-example.test",
            s["small"],
        )
    )
    story.append(Spacer(1, 0.25 * inch))

    header = Table(
        [
            ["Invoice #", "INV-2026-00148"],
            ["Issue date", "2026-02-15"],
            ["Due date", "2026-03-17"],
            ["Bill to", "Globex Industries · 1138 Test Street, Evergreen, OR"],
            ["Payment terms", "Net 30"],
            ["Tax ID", "EIN 00-0000000"],
        ],
        colWidths=[1.6 * inch, 4.5 * inch],
    )
    header.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#374151")),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 0.3 * inch))

    items = [
        ["#", "Item", "Qty", "Unit price", "Total"],
        ["1", "A4 Copier paper, 500-sheet ream", "12", "$8.50", "$102.00"],
        ["2", "Stapler, heavy-duty desktop", "3", "$22.00", "$66.00"],
        ["3", "Sticky notes assorted pack (24)", "5", "$14.40", "$72.00"],
        ["4", "Printer toner cartridge, black", "4", "$78.50", "$314.00"],
        ["5", "Whiteboard markers, 12-pack", "8", "$15.50", "$124.00"],
        ["6", "Document binder, 3-inch (set of 6)", "2", "$36.00", "$72.00"],
    ]
    table = Table(items, colWidths=[0.4 * inch, 3.5 * inch, 0.6 * inch, 1.0 * inch, 1.0 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 10),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    totals = Table(
        [
            ["Subtotal", "$750.00"],
            ["Tax (8%)", "$60.00"],
            ["Total due", "$810.00"],
        ],
        colWidths=[5.0 * inch, 1.1 * inch],
    )
    totals.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 11),
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
                ("TOPPADDING", (0, -1), (-1, -1), 6),
            ]
        )
    )
    story.append(totals)
    story.append(Spacer(1, 0.4 * inch))

    story.append(
        Paragraph(
            "Thank you for your business. Pay online at https://acme-example.test/pay/INV-2026-00148 or by wire to the account on file.",
            s["small"],
        )
    )

    doc.build(story)


def receipt() -> None:
    s = styles()
    doc = SimpleDocTemplate(
        str(HERE / "receipt.pdf"),
        pagesize=(4.0 * inch, 7.0 * inch),
        leftMargin=0.25 * inch,
        rightMargin=0.25 * inch,
        topMargin=0.25 * inch,
        bottomMargin=0.25 * inch,
        title="Receipt — BluePeak Cafe",
        author="BluePeak Cafe",
    )

    story: list = []
    story.append(Paragraph("BluePeak Cafe", s["h2"]))
    story.append(Paragraph("221B Brewing Lane · Portland, OR", s["small"]))
    story.append(Paragraph("Tel: (555) 010-0000", s["small"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Receipt #R-7733-A", s["body"]))
    story.append(Paragraph("Date: 2026-04-22 · 09:14", s["body"]))
    story.append(Paragraph("Server: Casey", s["body"]))
    story.append(Spacer(1, 0.1 * inch))

    items = [
        ["Item", "Qty", "Price"],
        ["Espresso, double", "1", "$3.50"],
        ["Oat milk latte", "1", "$5.25"],
        ["Almond croissant", "1", "$4.00"],
        ["Avocado toast", "1", "$11.50"],
    ]
    table = Table(items, colWidths=[2.0 * inch, 0.5 * inch, 1.0 * inch])
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.1 * inch))

    totals = Table(
        [
            ["Subtotal", "$24.25"],
            ["Tax", "$1.94"],
            ["Total", "$26.19"],
            ["Card (Visa ····4242)", "$26.19"],
        ],
        colWidths=[2.5 * inch, 1.0 * inch],
    )
    totals.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 9),
                ("FONT", (0, 2), (-1, 2), "Helvetica-Bold", 10),
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("LINEABOVE", (0, 2), (-1, 2), 0.75, colors.black),
                ("TOPPADDING", (0, 2), (-1, 2), 4),
            ]
        )
    )
    story.append(totals)
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Thank you — see you soon!", s["small"]))

    doc.build(story)


def contract() -> None:
    s = styles()
    doc = SimpleDocTemplate(
        str(HERE / "contract.pdf"),
        pagesize=LETTER,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
        title="Master Services Agreement — Globex & Nimbus Cloud",
        author="Globex Industries",
    )

    story: list = []
    story.append(Paragraph("MASTER SERVICES AGREEMENT", s["title"]))
    story.append(Spacer(1, 0.2 * inch))

    intro = (
        "This Master Services Agreement (the &quot;Agreement&quot;) is entered into as of "
        "<b>March 1, 2026</b> (the &quot;Effective Date&quot;) by and between <b>Globex Industries</b>, "
        "a Delaware corporation with its principal place of business at 1138 Test Street, "
        "Evergreen, OR (&quot;Client&quot;), and <b>Nimbus Cloud Services, LLC</b>, a fictitious limited "
        "liability company with its principal place of business at 99 Cumulus Way, "
        "Boulder, CO (&quot;Provider&quot;). Client and Provider may be referred to herein "
        "individually as a &quot;Party&quot; and collectively as the &quot;Parties.&quot;"
    )
    story.append(Paragraph(intro, s["body"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("1. Services", s["h2"]))
    story.append(
        Paragraph(
            "Provider shall provide the cloud infrastructure hosting and managed monitoring services described in one or more Statements of Work executed by the Parties from time to time. Each Statement of Work shall reference this Agreement and shall be governed by its terms.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("2. Term and Termination", s["h2"]))
    story.append(
        Paragraph(
            "This Agreement shall commence on the Effective Date and continue for an initial term of <b>twelve (12) months</b>, automatically renewing for successive one-year terms unless either Party provides written notice of non-renewal at least sixty (60) days prior to the end of the then-current term. Either Party may terminate this Agreement for material breach upon thirty (30) days' written notice if such breach remains uncured.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("3. Fees and Payment", s["h2"]))
    story.append(
        Paragraph(
            "Client shall pay Provider the fees set forth in each Statement of Work. The base monthly fee under this Agreement is <b>USD $4,800.00</b>, invoiced in advance. All invoices are due net thirty (30) days from the date of issue. Late payments accrue interest at 1.0% per month.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("4. Service Level Agreement", s["h2"]))
    story.append(
        Paragraph(
            "Provider commits to a target monthly uptime of 99.9% measured on a calendar-month basis. Service credits for missed SLA targets are detailed in Exhibit A.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("5. Confidentiality", s["h2"]))
    story.append(
        Paragraph(
            "Each Party shall hold the other's Confidential Information in strict confidence and use it solely for the purpose of performing under this Agreement. Confidentiality obligations survive termination for a period of three (3) years.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("6. Limitation of Liability", s["h2"]))
    story.append(
        Paragraph(
            "Neither Party's aggregate liability under this Agreement shall exceed the total fees paid by Client to Provider in the twelve (12) months preceding the event giving rise to the claim. Neither Party shall be liable for indirect, incidental, or consequential damages.",
            s["body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("7. Governing Law", s["h2"]))
    story.append(
        Paragraph(
            "This Agreement is governed by the laws of the State of Delaware, without regard to its conflict-of-law principles. The Parties consent to the exclusive jurisdiction of the courts located in Wilmington, Delaware.",
            s["body"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("Signatures", s["h2"]))
    story.append(Spacer(1, 0.4 * inch))

    sigs = Table(
        [
            ["GLOBEX INDUSTRIES", "NIMBUS CLOUD SERVICES, LLC"],
            ["", ""],
            ["By: _________________________", "By: _________________________"],
            ["Name: Jamie Rivera", "Name: Pat Mendez"],
            ["Title: Chief Procurement Officer", "Title: VP Sales"],
            ["Date: 2026-03-01", "Date: 2026-03-01"],
        ],
        colWidths=[3.0 * inch, 3.0 * inch],
    )
    sigs.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(sigs)

    story.append(Spacer(1, 0.4 * inch))
    story.append(
        Paragraph(
            "Synthetic example document — generated for the gemina-mcp examples. "
            "All names, addresses, and amounts are fictitious.",
            s["small"],
        )
    )

    doc.build(story)


def main() -> None:
    invoice()
    receipt()
    contract()
    for name in ("invoice.pdf", "receipt.pdf", "contract.pdf"):
        path = HERE / name
        print(f"  {name}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
