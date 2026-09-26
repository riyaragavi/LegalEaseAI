from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/test")
async def test_route():
    return {
        "message": "LegalEase API route is working!"
    }


@router.post("/generate")
async def generate_document(data: dict):

    document = f"""
LEGAL DOCUMENT
==============

Document Type:
{data.get("document_type", "")}

Parties:
{data.get("parties", "")}

Effective Date:
{data.get("effective_date", "")}

Jurisdiction:
{data.get("jurisdiction", "")}

Language:
{data.get("language", "")}

TERMS AND CONDITIONS
====================

{data.get("terms", "")}

IMPORTANT NOTICE
================

This document is an AI-generated draft for informational
and drafting purposes only. It should be reviewed by a
qualified legal professional before use.
"""

    return {
        "content": document
    }

from fastapi.responses import PlainTextResponse


@router.post("/export/txt")
async def export_txt(data: dict):

    content = data.get("content", "")

    return PlainTextResponse(
        content=content,
        media_type="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=legalease_document.txt"
        }
    )
from io import BytesIO
from docx import Document
from fastapi.responses import StreamingResponse


@router.post("/export/docx")
async def export_docx(data: dict):

    content = data.get("content", "")

    document = Document()

    for line in content.splitlines():
        document.add_paragraph(line)

    file_stream = BytesIO()
    document.save(file_stream)
    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": "attachment; filename=legalease_document.docx"
        }
    )

    from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@router.post("/export/pdf")
async def export_pdf(data: dict):

    content = data.get("content", "")

    file_stream = BytesIO()

    pdf = canvas.Canvas(file_stream, pagesize=A4)

    width, height = A4
    y = height - 50

    for line in content.splitlines():

        if y < 50:
            pdf.showPage()
            y = height - 50

        pdf.drawString(50, y, line[:100])
        y -= 18

    pdf.save()

    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=legalease_document.pdf"
        }
    )