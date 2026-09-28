"""HTTP schemas for requirement traceability links."""

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import RelationType


class RelationWrite(BaseModel):
    source_requirement_id: int = Field(gt=0)
    target_requirement_id: int = Field(gt=0)
    relation_type: RelationType
    is_directional: bool = True

    @model_validator(mode="after")
    def distinct_requirements(self):
        if self.source_requirement_id == self.target_requirement_id:
            raise ValueError("A requirement cannot be related to itself")
        return self


class RelationRead(RelationWrite):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RelationUpdate(BaseModel):
    relation_type: RelationType | None = None
    is_directional: bool | None = None
