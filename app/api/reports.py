"""WeasyPrint PDF reporting for current REQS project data."""

from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, Response
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PriorityScore, Requirement, RequirementRelation
from app.utils.charts import METHOD_LABELS, score_bars


router = APIRouter(prefix="/reports", tags=["reports"])
TEMPLATE_DIRECTORY = Path(__file__).resolve().parents[1] / "templates"
environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIRECTORY),
    autoescape=select_autoescape(["html", "xml"]),
)
RELATION_CODES = {
    "depends_on": "DEP",
    "prerequisite_of": "PRE",
    "similar_to": "SIM",
    "refines": "REF",
    "conflicts_with": "CON",
    "related_to": "REL",
}


def report_context(db: Session) -> dict:
    """Build one auditable report context from persisted project data."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.key)))
    scores = db.execute(
        select(PriorityScore, Requirement)
        .join(Requirement)
        .order_by(PriorityScore.method, PriorityScore.normalized_score.desc(), Requirement.key)
    ).all()
    results = [
        {
            "requirement_key": requirement.key,
            "requirement_title": requirement.title,
            "method": score.method.value,
            "method_label": METHOD_LABELS[score.method.value],
            "raw_score": f"{float(score.raw_score):.4f}",
            "normalized_score": f"{float(score.normalized_score):.2f}",
        }
        for score, requirement in scores
    ]
    matrix: dict[tuple[int, int], str] = {}
    impacts = []
    for relation in db.scalars(select(RequirementRelation)):
        matrix[(relation.source_requirement_id, relation.target_requirement_id)] = RELATION_CODES[relation.relation_type.value]
        source = db.get(Requirement, relation.source_requirement_id)
        target = db.get(Requirement, relation.target_requirement_id)
        if source and target:
            impacts.append(
                {
                    "source": source.key,
                    "target": target.key,
                    "relation_type": relation.relation_type.value,
                }
            )
        if not relation.is_directional:
            matrix[(relation.target_requirement_id, relation.source_requirement_id)] = RELATION_CODES[relation.relation_type.value]
    return {
        "generated_on": date.today().isoformat(),
        "requirements": requirements,
        "results": results,
        "matrix": matrix,
        "impacts": impacts,
        "score_chart": score_bars(results),
        "relation_codes": RELATION_CODES,
    }


def build_pdf_bytes(db: Session) -> bytes:
    """Render the report with WeasyPrint; imported lazily for testability outside Docker."""
    from weasyprint import HTML

    html = environment.get_template("report.html").render(**report_context(db))
    return HTML(string=html, base_url=str(TEMPLATE_DIRECTORY)).write_pdf()


@router.get("/pdf")
def export_pdf_report(db: Session = Depends(get_db)) -> Response:
    """Export a printable report with methods, priorities, chart, matrix and impact summary."""
    return Response(
        content=build_pdf_bytes(db),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reqs-karar-destek-raporu.pdf"},
    )
