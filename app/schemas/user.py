from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from app.utils.enums import UserRole


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)