"""Request and response schemas for AHP pairwise comparisons."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AhpComparisonWrite(BaseModel):
    left_requirement_id: int = Field(gt=0)
    right_requirement_id: int = Field(gt=0)
    comparison_value: str = Field(min_length=1, max_length=8)


class AhpComparisonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    requirement_a_id: int
    requirement_b_id: int
    comparison_value: Decimal
