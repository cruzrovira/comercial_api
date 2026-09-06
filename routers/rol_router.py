from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from models.rol import Rol, RolCreate, RolUpdate
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia


router = APIRouter()


@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
def get_roles(session: SessionDeDependencia,
              offset: int = Query(0, ge=0),
              limit: int = Query(20, ge=1)):

    consulta = select(Rol).offset(offset).limit(
        limit)  # Limitar a 'limit' resultados por defecto
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()
    # return  session.exec(select(Rol)).all()


@router.get("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def get_rol(id: int, session: SessionDeDependencia):
    consulta = select(Rol).where(
        Rol.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return resultado_de_consulta


@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
def create_rol(datos_rol: RolCreate, session: SessionDeDependencia):
    rol_nuevo = Rol(
        nombre=datos_rol.nombre, descripcion=datos_rol.descripcion)
    session.add(rol_nuevo)
    session.commit()
    session.refresh(rol_nuevo)
    return rol_nuevo


@router.delete("/roles/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rol(id: int, session: SessionDeDependencia):
    consulta = select(Rol).where(
        Rol.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    # verificación si existe un rol con ese id
    if not resultado_de_consulta:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    # eliminación del rol
    session.delete(resultado_de_consulta)
    # ejecuta la consulta en la base de datos
    session.commit()
    return None


@router.put("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
def update_rol(id: int, datos_rol: RolUpdate, session: SessionDeDependencia):
    consulta = select(Rol).where(Rol.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    # verificación si existe un rol con ese id
    if not resultado_de_consulta:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    # actualización de datos
    resultado_de_consulta.nombre = datos_rol.nombre
    # actualización de la descripción solo si se proporciona un valor
    if datos_rol.descripcion is not None:
        resultado_de_consulta.descripcion = datos_rol.descripcion

    resultado_de_consulta.updated_at = datetime.utcnow()
    # agregar la consulta a la session
    session.add(resultado_de_consulta)
    # ejecuta la consulta en la base de datos
    session.commit()
    session.refresh(resultado_de_consulta)
    return resultado_de_consulta
