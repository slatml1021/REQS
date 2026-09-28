"""FastAPI application entry point."""

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.requirements import router as requirements_router
from app.api.ahp import router as ahp_router
from app.api.volere import router as volere_router
from app.api.results import router as results_router
from app.api.traceability import router as traceability_router
from app.api.wiegers import router as wiegers_router
from app.api.relations import router as relations_router
from app.api.impact import router as impact_router
from app.api.reports import router as reports_router
from app.database import get_db
from app.models import Requirement


app = FastAPI(title="REQS API", version="0.1.0")
app.include_router(requirements_router, prefix="/api/v1")
app.include_router(ahp_router, prefix="/api/v1")
app.include_router(volere_router, prefix="/api/v1")
app.include_router(results_router, prefix="/api/v1")
app.include_router(traceability_router, prefix="/api/v1")
app.include_router(wiegers_router, prefix="/api/v1")
app.include_router(relations_router, prefix="/api/v1")
app.include_router(impact_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get("/")
def workspace(request: Request):
    """Render the REQS project workspace."""
    return templates.TemplateResponse(request, "workspace.html")


@app.get("/ahp/comparisons")
def ahp_comparisons(request: Request, db: Session = Depends(get_db)):
    """Render the first AHP pairwise-comparison input screen."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.key)))
    return templates.TemplateResponse(request, "ahp_comparisons.html", {"requirements": requirements})


@app.get("/volere/scoring")
def volere_scoring(request: Request, db: Session = Depends(get_db)):
    """Render the initial Volere criteria and scoring screen."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.key)))
    return templates.TemplateResponse(request, "volere_scoring.html", {"requirements": requirements})


@app.get("/traceability/graph")
def traceability_graph(request: Request):
    """Render the interactive requirement relation graph."""
    return templates.TemplateResponse(request, "traceability_graph.html")


@app.get("/traceability/matrix")
def traceability_matrix_screen(request: Request):
    return templates.TemplateResponse(request, "traceability_matrix.html")


@app.get("/wiegers/scoring")
def wiegers_scoring(request: Request):
    return templates.TemplateResponse(request, "wiegers_scoring.html")


@app.get("/impact-analysis")
def impact_analysis_screen(request: Request):
    return templates.TemplateResponse(request, "impact_analysis.html")


@app.get("/prioritization/dashboard")
def prioritization_dashboard(request: Request):
    """Render the method-neutral priority result screen."""
    return templates.TemplateResponse(request, "prioritization_dashboard.html")
