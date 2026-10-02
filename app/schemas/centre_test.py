from decimal import Decimal

from pydantic import BaseModel, Field


class CentreTestCreate(BaseModel):
    test_id: int
    price: Decimal = Field(gt=0)


class CentreTestUpdate(BaseModel):
    price: Decimal = Field(gt=0)


class CentreTestResponse(BaseModel):
    id: int
    centre_id: int
    test_id: int
    price: Decimal


class CentreTestPublicResponse(BaseModel):
    id: int
    test_id: int
    test_name: str
    price: Decimal