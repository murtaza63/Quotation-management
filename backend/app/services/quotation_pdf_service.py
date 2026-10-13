from io import BytesIO
from pathlib import Path
from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


class QuotationPDFService:

    @staticmethod
    def amount_in_words(amount):
        amount = amount or 0
        amount = round(float(amount), 2)

        dirhams = int(amount)
        fils = round((amount - dirhams) * 100)

        # Handle rounding that produces 100 fils.
        if fils == 100:
            dirhams += 1
            fils = 0

        dirham_words = num2words(
            dirhams,
            lang="en",
        ).replace("-", " ")

        if fils > 0:
            fils_words = num2words(
                fils,
                lang="en",
            ).replace("-", " ")

            return (
                f"{dirham_words.title()} Dirhams " f"and {fils_words.title()} Fils Only"
            )

        return f"{dirham_words.title()} Dirhams Only"

    @staticmethod
    def generate_pdf(quotation):
        buffer = BytesIO()

        # ---------------------------------------------------------
        # DOCUMENT
        # ---------------------------------------------------------

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=35 * mm,
            bottomMargin=35 * mm,
        )

        # ---------------------------------------------------------
        # LETTERHEAD
        # ---------------------------------------------------------

        base_dir = Path(__file__).resolve().parent.parent
        letterhead_path = base_dir / "assets" / "letterhead.jpg"

        if not letterhead_path.exists():
            raise FileNotFoundError(f"Letterhead image not found: {letterhead_path}")

        def draw_letterhead(canvas, document):
            canvas.saveState()

            canvas.drawImage(
                str(letterhead_path),
                0,
                0,
                width=A4[0],
                height=A4[1],
                preserveAspectRatio=False,
                mask="auto",
            )

            canvas.restoreState()

        # ---------------------------------------------------------
        # STYLES
        # ---------------------------------------------------------

        styles = getSampleStyleSheet()

        quotation_title_style = ParagraphStyle(
            "QuotationTitle",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=4,
        )

        quotation_number_style = ParagraphStyle(
            "QuotationNumber",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.grey,
            spaceAfter=12,
        )

        section_style = ParagraphStyle(
            "Section",
            parent=styles["Heading3"],
            fontSize=11,
            leading=14,
            spaceBefore=4,
            spaceAfter=6,
        )

        normal_style = ParagraphStyle(
            "NormalCustom",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
        )
        amount_words_style = ParagraphStyle(
            "AmountWords",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            wordWrap="LTR",
        )

        right_style = ParagraphStyle(
            "Right",
            parent=normal_style,
            alignment=TA_RIGHT,
        )

        # ---------------------------------------------------------
        # STORY
        # ---------------------------------------------------------

        story = []

        # ---------------------------------------------------------
        # QUOTATION TITLE
        # ---------------------------------------------------------

        story.append(
            Paragraph(
                "<b>QUOTATION</b>",
                quotation_title_style,
            )
        )

        story.append(
            Paragraph(
                quotation.quotation_number,
                quotation_number_style,
            )
        )

        # ---------------------------------------------------------
        # QUOTATION INFORMATION
        # ---------------------------------------------------------

        quotation_info = [
            [
                Paragraph("<b>Quotation Date</b>", normal_style),
                str(quotation.quotation_date),
                Paragraph("<b>Valid Until</b>", normal_style),
                str(quotation.valid_until),
            ],
            [
                Paragraph("<b>Status</b>", normal_style),
                str(quotation.status).upper(),
                Paragraph("<b>VAT</b>", normal_style),
                f"{quotation.vat_percentage:.2f}%",
            ],
        ]

        quotation_table = Table(
            quotation_info,
            colWidths=[
                35 * mm,
                55 * mm,
                30 * mm,
                55 * mm,
            ],
        )

        quotation_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.lightgrey,
                    ),
                    (
                        "BACKGROUND",
                        (2, 0),
                        (2, -1),
                        colors.lightgrey,
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(quotation_table)
        story.append(Spacer(1, 14))

        # ---------------------------------------------------------
        # CUSTOMER
        # ---------------------------------------------------------

        story.append(
            Paragraph(
                "<b>Customer</b>",
                section_style,
            )
        )

        customer = quotation.customer

        customer_data = [
            [
                Paragraph("<b>Company</b>", normal_style),
                customer.company_name,
            ],
            [
                Paragraph("<b>Contact Person</b>", normal_style),
                customer.contact_person or "",
            ],
            [
                Paragraph("<b>Phone</b>", normal_style),
                customer.phone or "",
            ],
            [
                Paragraph("<b>Email</b>", normal_style),
                customer.email or "",
            ],
        ]

        customer_table = Table(
            customer_data,
            colWidths=[
                40 * mm,
                135 * mm,
            ],
        )

        customer_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.lightgrey,
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(customer_table)
        story.append(Spacer(1, 12))

        # ---------------------------------------------------------
        # ITEMS
        # ---------------------------------------------------------

        story.append(
            Paragraph(
                "<b>Items</b>",
                section_style,
            )
        )

        item_data = [
            [
                Paragraph("<b>Description</b>", normal_style),
                Paragraph("<b>Quantity</b>", normal_style),
                Paragraph("<b>Unit</b>", normal_style),
                Paragraph("<b>Unit Price</b>", normal_style),
                Paragraph("<b>Total</b>", normal_style),
            ]
        ]
        if quotation.items:
            for item in quotation.items:
                item_data.append(
                    [
                        Paragraph(item.description, normal_style),
                        Paragraph(f"{item.quantity:.2f}", normal_style),
                        Paragraph(item.unit, normal_style),
                        Paragraph(f"AED {item.unit_price:.2f}", normal_style),
                        Paragraph(f"AED {item.total:.2f}", normal_style),
                    ]
                )
        else:
            item_data.append(
                [
                    Paragraph("No items available", normal_style),
                    "",
                    "",
                    "",
                    "",
                ]
            )

        items_table = Table(
            item_data,
            colWidths=[
                90 * mm,
                20 * mm,
                20 * mm,
                30 * mm,
                30 * mm,
            ],
            repeatRows=1,
        )

        items_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    # Grid
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    # Alignment
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    # Padding
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    # Font
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                ]
            )
        )

        story.append(items_table)
        story.append(Spacer(1, 12))

        # ---------------------------------------------------------
        # SUMMARY
        # ---------------------------------------------------------
        amount_words = QuotationPDFService.amount_in_words(quotation.total_amount or 0)

        summary_data = [
            [
                Paragraph("Subtotal", normal_style),
                Paragraph(
                    f"AED {float(quotation.subtotal):,.2f}",
                    right_style,
                ),
            ],
            [
                Paragraph(
                    f"VAT ({float(quotation.vat_percentage):.2f}%)",
                    normal_style,
                ),
                Paragraph(
                    f"AED  {float(quotation.vat_amount):,.2f}",
                    right_style,
                ),
            ],
            [
                Paragraph(
                    "<b>Total Amount</b>",
                    normal_style,
                ),
                Paragraph(
                    f"<b>AED {float(quotation.total_amount):,.2f}</b>",
                    right_style,
                ),
            ],
        ]

        summary_table = Table(
            summary_data,
            colWidths=[
                135 * mm,
                40 * mm,
            ],
        )

        summary_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "ALIGN",
                        (1, 0),
                        (1, -1),
                        "RIGHT",
                    ),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    (
                        "BACKGROUND",
                        (0, 2),
                        (-1, 2),
                        colors.lightgrey,
                    ),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(summary_table)
        story.append(Spacer(1, 8))

        # ---------------------------------------------------------
        # AMOUNT IN WORDS
        # ---------------------------------------------------------
        amount_words_table = Table(
            [
                [
                    Paragraph("<b>Amount in Words:</b>", amount_words_style),
                    Paragraph(amount_words, amount_words_style),
                ]
            ],
            colWidths=[35 * mm, 140 * mm],
            hAlign="LEFT",
        )
        amount_words_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(amount_words_table)
        story.append(Spacer(1, 12))
        # ---------------------------------------------------------
        # NOTES
        # ---------------------------------------------------------

        if quotation.notes:
            story.append(
                Paragraph(
                    "<b>Notes</b>",
                    section_style,
                )
            )

            story.append(
                Paragraph(
                    quotation.notes,
                    normal_style,
                )
            )

        # ---------------------------------------------------------
        # SIGNATURE / APPROVAL
        # ---------------------------------------------------------

        story.append(Spacer(1, 12))

        signature_data = [
            [
                Paragraph(
                    "<b>Prepared By</b>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Authorized Signature</b>",
                    normal_style,
                ),
            ],
            [
                Paragraph(
                    "Pure Golden Wrecking &amp; Demolition Works L.L.C.",
                    normal_style,
                ),
                Paragraph(
                    "Name: __________________________",
                    normal_style,
                ),
            ],
            [
                Paragraph(
                    "Name: __________________________",
                    normal_style,
                ),
                Paragraph(
                    "Signature: _____________________",
                    normal_style,
                ),
            ],
            [
                Paragraph(
                    "Date: __________________________",
                    normal_style,
                ),
                Paragraph(
                    "Date: __________________________",
                    normal_style,
                ),
            ],
        ]

        signature_table = Table(
            signature_data,
            colWidths=[
                87.5 * mm,
                87.5 * mm,
            ],
        )

        signature_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.grey),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )

        story.append(KeepTogether([signature_table]))

        # ---------------------------------------------------------
        # BUILD PDF
        # ---------------------------------------------------------

        document.build(
            story,
            onFirstPage=draw_letterhead,
            onLaterPages=draw_letterhead,
        )

        buffer.seek(0)

        return buffer
