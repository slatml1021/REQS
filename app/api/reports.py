"""Portable PDF reporting for current REQS project data."""

from datetime import date
from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, Depends, Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PriorityScore, Requirement, RequirementRelation


router = APIRouter(prefix="/reports", tags=["reports"])
FONT_NAME = "REQSUnicode"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
if FONT_PATH.exists():
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
else:  # Keeps local development functional on non-macOS systems.
    FONT_NAME = "Helvetica"


@router.get("/pdf")
def export_pdf_report(db: Session = Depends(get_db)) -> Response:
    """Export requirement priorities and traceability matrix as a PDF."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.key)))
    id_to_key = {requirement.id: requirement.key for requirement in requirements}
    scores = db.execute(select(PriorityScore, Requirement).join(Requirement).order_by(PriorityScore.method, PriorityScore.normalized_score.desc())).all()
    cells = {(relation.source_requirement_id, relation.target_requirement_id): relation.relation_type.value for relation in db.scalars(select(RequirementRelation))}
    styles = getSampleStyleSheet()
    for style in (styles["Title"], styles["Heading2"], styles["Normal"]):
        style.fontName = FONT_NAME
    story = [Paragraph("REQS Karar Destek Raporu", styles["Title"]), Paragraph(f"Tarih: {date.today().isoformat()} - Önceliklendirme ve izlenebilirlik özeti", styles["Normal"]), Spacer(1, 7 * mm), Paragraph("Önceliklendirme sonuçları", styles["Heading2"])]
    priority_rows = [["Anahtar", "Gereksinim", "Yöntem", "Normalize puan"]] + [[requirement.key, requirement.title, score.method.value.upper(), f"{float(score.normalized_score):.2f}"] for score, requirement in scores]
    if len(priority_rows) == 1:
        priority_rows.append(["—", "Henüz puanlanmış gereksinim yok.", "—", "—"])
    priority_table = Table(priority_rows, colWidths=[26 * mm, 87 * mm, 30 * mm, 32 * mm])
    story += [priority_table, Spacer(1, 7 * mm), Paragraph("İzlenebilirlik matrisi", styles["Heading2"])]
    matrix_rows = [["Kaynak / Hedef"] + [requirement.key for requirement in requirements]]
    matrix_rows += [[source.key] + [cells.get((source.id, target.id), "—") for target in requirements] for source in requirements]
    if len(matrix_rows) == 1:
        matrix_rows.append(["Henüz gereksinim yok."])
    width = 175 * mm / max(len(matrix_rows[0]), 1)
    matrix_table = Table(matrix_rows, colWidths=[width] * len(matrix_rows[0]))
    for table in (priority_table, matrix_table):
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#123F71")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D8E0EA")), ("FONTNAME", (0, 0), (-1, -1), FONT_NAME), ("FONTSIZE", (0, 0), (-1, -1), 8), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [matrix_table, Spacer(1, 6 * mm), Paragraph("Bu rapor REQS sistemindeki güncel kayıtlar üzerinden otomatik üretilmiştir.", styles["Normal"])]
    buffer = BytesIO()
    SimpleDocTemplate(buffer, pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm, topMargin=17 * mm, bottomMargin=17 * mm).build(story)
    return Response(content=buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=reqs-karar-destek-raporu.pdf"})
