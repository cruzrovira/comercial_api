from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr
from typing import Optional


class UsuarioBase(SQLModel):
    username: str = Field(nullable=False, max_length=50,
                          min_length=3, unique=True)

    password: str = Field(nullable=False, max_length=255,
                          min_length=3)
    nombre: str = Field(nullable=False, max_length=255,
                        min_length=3)
    apellido: str = Field(nullable=False, max_length=255,
                          min_length=3)
    telefono: str = Field(nullable=False, max_length=9,
                          min_length=9)
    correo: Optional[EmailStr] = Field(default=None, max_length=255)
    id_rol: int = Field(nullable=False, foreign_key="roles.id")


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow)


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(UsuarioBase):
    pass


class UsuarioUpdatePatch(SQLModel):
    username: Optional[str] = Field(default=None, max_length=50,
                                    min_length=3)

    password: Optional[str] = Field(default=None, max_length=255,
                                    min_length=3)
    nombre: Optional[str] = Field(default=None, max_length=255,
                                  min_length=3)
    apellido: Optional[str] = Field(default=None, max_length=255,
                                    min_length=3)
    telefono: Optional[str] = Field(default=None, max_length=9,
                                    min_length=9)
    correo: Optional[EmailStr] = Field(default=None, max_length=255)
    id_rol: Optional[int] = Field(default=None)
