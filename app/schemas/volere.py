"""Request and response schemas for Volere prioritization."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class VolereCriterion(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    weight: Decimal = Field(ge=0, le=100)
    score: Decimal = Field(ge=0, le=10)


class VolereScoreWrite(BaseModel):
    requirement_id: int = Field(gt=0)
    criteria: list[VolereCriterion] = Field(min_length=1, max_length=4)


class VolereScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    requirement_id: int
    raw_score: Decimal
    normalized_score: Decimal
    inputs: dict
