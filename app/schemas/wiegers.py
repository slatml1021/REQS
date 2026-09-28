"""HTTP schemas for Wiegers relative-weighting assessments."""

from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class WiegersWeights(BaseModel):
    benefit: Decimal = Field(gt=0, le=10)
    penalty: Decimal = Field(gt=0, le=10)
    cost: Decimal = Field(gt=0, le=10)
    risk: Decimal = Field(gt=0, le=10)


class WiegersAssessment(BaseModel):
    requirement_id: int = Field(gt=0)
    benefit: Decimal = Field(ge=1, le=9)
    penalty: Decimal = Field(ge=1, le=9)
    cost: Decimal = Field(ge=1, le=9)
    risk: Decimal = Field(ge=1, le=9)


class WiegersBatchWrite(BaseModel):
    weights: WiegersWeights
    assessments: list[WiegersAssessment] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_requirements(self):
        ids = [assessment.requirement_id for assessment in self.assessments]
        if len(ids) != len(set(ids)):
            raise ValueError("Each requirement can be assessed only once per request")
        return self
