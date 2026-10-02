from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CentreCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=500)


class CentreUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    location: str | None = Field(default=None, min_length=1, max_length=500)
    is_active: bool | None = None


class CentreResponse(BaseModel):
    id: int
    name: str
    location: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)