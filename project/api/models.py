from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegistration(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    phone: Optional[str] = Field(None, min_length=9, max_length=15)
    city: Optional[str] = Field(None, min_length=2)