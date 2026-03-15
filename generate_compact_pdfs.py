#!/usr/bin/env python3
"""
Generate compact PDFs from DBBP42 markdown documents.
Uses reportlab with tight margins and smaller fonts for space efficiency.
"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Page dimensions - compact A4 with tight margins
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 15 * mm
RIGHT_MARGIN = 15 * mm
TOP_MARGIN = 15 * mm
BOTTOM_MARGIN = 15 * mm

def create_compact_styles():
    """Create compact paragraph styles for space efficiency."""
    styles = getSampleStyleSheet()

    # Compact title style
    styles.add(ParagraphStyle(
        name='CompactTitle',
        fontSize=14,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=4 * mm,
        spaceBefore=0,
        fontName='Helvetica-Bold'
    ))

    # Header for document (DBBP42 Statut)
    styles.add(ParagraphStyle(
        name='DocHeader',
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=3 * mm,
        spaceBefore=0,
        fontName='Helvetica-Bold',
        textColor=colors.grey
    ))

    # Main heading (H1)
    styles.add(ParagraphStyle(
        name='CompactH1',
        fontSize=12,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=3 * mm,
        spaceBefore=4 * mm,
        fontName='Helvetica-Bold'
    ))

    # Section heading (H2)
    styles.add(ParagraphStyle(
        name='CompactH2',
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=2 * mm,
        spaceBefore=3 * mm,
        fontName='Helvetica-Bold'
    ))

    # Subsection heading (H3)
    styles.add(ParagraphStyle(
        name='CompactH3',
        fontSize=9,
        leading=11,
        alignment=TA_LEFT,
        spaceAfter=1.5 * mm,
        spaceBefore=2 * mm,
        fontName='Helvetica-Bold'
    ))

    # H4 heading
    styles.add(ParagraphStyle(
        name='CompactH4',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        spaceAfter=1 * mm,
        spaceBefore=1.5 * mm,
        fontName='Helvetica-BoldOblique'
    ))

    # Body text - compact
    styles.add(ParagraphStyle(
        name='CompactBody',
        fontSize=8,
        leading=10,
        alignment=TA_JUSTIFY,
        spaceAfter=1.5 * mm,
        spaceBefore=0,
        fontName='Helvetica'
    ))

    # List item
    styles.add(ParagraphStyle(
        name='CompactList',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        spaceAfter=0.5 * mm,
        spaceBefore=0,
        leftIndent=5 * mm,
        fontName='Helvetica'
    ))

    # Bold text style
    styles.add(ParagraphStyle(
        name='CompactBold',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        spaceAfter=1 * mm,
        spaceBefore=0,
        fontName='Helvetica-Bold'
    ))

    # Small text for footer/notes
    styles.add(ParagraphStyle(
        name='CompactSmall',
        fontSize=7,
        leading=9,
        alignment=TA_LEFT,
        spaceAfter=1 * mm,
        spaceBefore=0,
        fontName='Helvetica-Oblique',
        textColor=colors.grey
    ))

    # Signature block
    styles.add(ParagraphStyle(
        name='Signature',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        spaceAfter=0.5 * mm,
        spaceBefore=0,
        fontName='Helvetica'
    ))

    return styles

def parse_markdown_line(line, styles):
    """Parse a single markdown line and return appropriate flowable."""
    line = line.rstrip()

    # Empty line
    if not line:
        return Spacer(1, 1 * mm)

    # Horizontal rule
    if line.strip() in ['---', '***', '___']:
        return Spacer(1, 2 * mm)

    # Headers
    if line.startswith('#### '):
        text = process_inline_formatting(line[5:])
        return Paragraph(text, styles['CompactH4'])
    elif line.startswith('### '):
        text = process_inline_formatting(line[4:])
        return Paragraph(text, styles['CompactH3'])
    elif line.startswith('## '):
        text = process_inline_formatting(line[3:])
        return Paragraph(text, styles['CompactH2'])
    elif line.startswith('# '):
        text = process_inline_formatting(line[2:])
        return Paragraph(text, styles['CompactH1'])

    # List items
    if line.strip().startswith('- '):
        text = process_inline_formatting(line.strip()[2:])
        return Paragraph(f"- {text}", styles['CompactList'])

    # Numbered list
    match = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
    if match:
        num, text = match.groups()
        text = process_inline_formatting(text)
        return Paragraph(f"{num}. {text}", styles['CompactList'])

    # Regular paragraph
    text = process_inline_formatting(line)
    return Paragraph(text, styles['CompactBody'])

def process_inline_formatting(text):
    """Convert markdown inline formatting to reportlab XML tags."""
    # Bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic: *text* -> <i>text</i>
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    # Escape special chars for XML
    text = text.replace('&', '&amp;')
    # Fix escaped special chars
    text = text.replace('&amp;amp;', '&amp;')
    return text

def parse_table(lines, start_idx, styles):
    """Parse a markdown table starting at given index."""
    table_lines = []
    i = start_idx

    while i < len(lines) and lines[i].strip().startswith('|'):
        table_lines.append(lines[i])
        i += 1

    if len(table_lines) < 2:
        return None, start_idx

    # Parse header
    header = [cell.strip() for cell in table_lines[0].strip('|').split('|')]

    # Skip separator line
    data_start = 2 if len(table_lines) > 1 and re.match(r'^[\|\s\-:]+$', table_lines[1]) else 1

    # Parse data rows
    rows = [header]
    for line in table_lines[data_start:]:
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        rows.append(cells)

    # Create table with compact styling
    col_count = len(header)
    available_width = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
    col_widths = [available_width / col_count] * col_count

    # Adjust widths if needed
    if col_count >= 4:
        col_widths = None  # Auto-calculate

    table = Table(rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('LEADING', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))

    return table, i

def markdown_to_flowables(markdown_text, styles, doc_header=None):
    """Convert markdown text to reportlab flowables."""
    flowables = []
    lines = markdown_text.split('\n')

    # Add document header if specified
    if doc_header:
        flowables.append(Paragraph(doc_header, styles['DocHeader']))
        flowables.append(Spacer(1, 2 * mm))

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for table
        if line.strip().startswith('|'):
            table, new_i = parse_table(lines, i, styles)
            if table:
                flowables.append(Spacer(1, 1 * mm))
                flowables.append(table)
                flowables.append(Spacer(1, 1 * mm))
                i = new_i
                continue

        flowable = parse_markdown_line(line, styles)
        if flowable:
            flowables.append(flowable)

        i += 1

    return flowables

def add_page_number(canvas, doc):
    """Add page number to each page."""
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.grey)
    page_num = canvas.getPageNumber()
    text = f"Stran {page_num}"
    canvas.drawCentredString(PAGE_WIDTH / 2, 10 * mm, text)
    canvas.restoreState()

def generate_pdf(markdown_file, pdf_file, doc_header=None):
    """Generate a compact PDF from markdown file."""
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Create styles
    styles = create_compact_styles()

    # Create document with tight margins
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )

    # Convert markdown to flowables
    flowables = markdown_to_flowables(markdown_content, styles, doc_header)

    # Build PDF
    doc.build(flowables, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Generated: {pdf_file}")

def main():
    import os

    base_dir = "/home/diablo/Projects/DBBP"

    # Generate statute PDF with header
    generate_pdf(
        os.path.join(base_dir, "statut-dbbp42.md"),
        os.path.join(base_dir, "statut-dbbp42.pdf"),
        doc_header="DBBP42 Statut"
    )

    # Generate zapisnik PDF
    generate_pdf(
        os.path.join(base_dir, "zapisnik-ustavni-zbor-dbbp42.md"),
        os.path.join(base_dir, "zapisnik-ustavni-zbor-dbbp42.pdf"),
        doc_header=None
    )

    print("\nDone! Both compact PDFs have been generated.")

if __name__ == "__main__":
    main()
