"""FastAPI application entry point."""

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.requirements import router as requirements_router
from app.database import get_db
from app.models import Requirement


app = FastAPI(title="REQS API", version="0.1.0")
app.include_router(requirements_router, prefix="/api/v1")

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get("/ahp/comparisons")
def ahp_comparisons(request: Request, db: Session = Depends(get_db)):
    """Render the first AHP pairwise-comparison input screen."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.key)))
    return templates.TemplateResponse(request, "ahp_comparisons.html", {"requirements": requirements})
