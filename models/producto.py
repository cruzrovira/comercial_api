from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductoBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100, min_length=4)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio_compra: Decimal = Field(nullable=False, gt=0)
    precio_venta: Decimal = Field(nullable=False, gt=0)
    stock: int = Field(nullable=False, ge=0)
    imagen: str = Field(nullable=False, max_length=255)
    id_categoria: int = Field(nullable=False, foreign_key="categorias.id")


class Producto(ProductoBase, table=True):
    __tablename__ = "productos"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoUpdatePatch(SQLModel):
    nombre: Optional[str] = Field(None, max_length=100, min_length=4)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio_compra: Optional[Decimal] = Field(None, gt=0)
    precio_venta: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    imagen: Optional[str] = Field(None, max_length=255)
    id_categoria: Optional[int] = Field(None)
