"""HTTP schemas for requirements."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RequirementCreate(BaseModel):
    key: str = Field(min_length=1, max_length=32, pattern=r"^[A-Za-z0-9_-]+$")
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    requirement_type: str = Field(default="functional", min_length=1, max_length=32)
    status: str = Field(default="draft", min_length=1, max_length=32)


class RequirementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    requirement_type: str | None = Field(default=None, min_length=1, max_length=32)
    status: str | None = Field(default=None, min_length=1, max_length=32)


class RequirementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    title: str
    description: str | None
    requirement_type: str
    status: str
    created_at: datetime
    updated_at: datetime
