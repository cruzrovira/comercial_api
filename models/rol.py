from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class RolBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=255,
                        min_length=3)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class Rol(RolBase, table=True):
    __tablename__ = "roles"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow)


class RolCreate(RolBase):
    pass


class RolUpdate(RolBase):
    pass
