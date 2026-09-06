from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class CategoriaBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=255,
                        min_length=3)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class Categoria(CategoriaBase, table=True):
    __tablename__ = "categorias"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass
