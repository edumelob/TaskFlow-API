"""
Schemas Pydantic: contratos de entrada (request) e saída (response) da API.
Mantidos separados dos modelos ORM por boa prática (nunca expor o modelo de banco direto).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- User ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Mínimo de 8 caracteres")
    full_name: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    created_at: datetime


# ---------- Auth ----------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ---------- Task ----------

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    owner_id: int
