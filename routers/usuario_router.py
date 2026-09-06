

from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.rol import Rol
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioUpdatePatch
from datetime import datetime
from lib.pwd import get_password_hash
router = APIRouter()


@router.get("/usuarios", response_model=list[Usuario], status_code=status.HTTP_200_OK)
async def get_usuarios(session: SessionDeDependencia,
                       offset: int = Query(
                           0, ge=0),
                       limit: int = Query(
                           100, ge=1,
                       )):
    consulta = select(Usuario).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuario no encontrado")
    return resultado_de_consulta


@router.post('/usuarios', response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def create_usuario(datos_usuario: UsuarioCreate, session: SessionDeDependencia):

    usuario_nuevo = Usuario(
        password=get_password_hash(datos_usuario.password),
        nombre=datos_usuario.nombre,
        apellido=datos_usuario.apellido,
        telefono=datos_usuario.telefono,
    )

    consulta = select(Usuario).where(
        Usuario.username == datos_usuario.username)
    usuario_existente = session.exec(consulta).first()
    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El nombre de usuario ya está en uso")

    usuario_nuevo.username = datos_usuario.username
    if datos_usuario.correo:
        usuario_nuevo.correo = datos_usuario.correo

    if datos_usuario.id_rol:
        consulta = select(Rol).where(Rol.id == datos_usuario.id_rol)
        rol = session.exec(consulta).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Rol no encontrado")

    usuario_nuevo.id_rol = datos_usuario.id_rol
    session.add(usuario_nuevo)
    session.commit()
    session.refresh(usuario_nuevo)
    return usuario_nuevo


@router.delete('/usuarios/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuario no encontrado")
    session.delete(resultado_de_consulta)
    session.commit()
    return None


@router.put('/usuarios/{id}', response_model=Usuario, status_code=status.HTTP_200_OK)
async def update_usuario(id: int, datos_usuario: UsuarioUpdate, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    usuario = session.exec(consulta).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Usuario no encontrado')

    if datos_usuario.id_rol:
        consulta = select(Rol).where(Rol.id == datos_usuario.id_rol)
        rol = session.exec(consulta).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Rol no encontrado")

    if datos_usuario.correo:
        usuario.correo = datos_usuario.correo

    usuario.username = datos_usuario.username
    usuario.nombre = datos_usuario.nombre
    usuario.apellido = datos_usuario.apellido
    usuario.telefono = datos_usuario.telefono
    usuario.id_rol = datos_usuario.id_rol
    usuario.updated_at = datetime.utcnow()

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.patch('/usuarios/{id}', response_model=Usuario, status_code=status.HTTP_200_OK)
async def patch_usuario(id: int, datos_usuario: UsuarioUpdatePatch, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    usuario = session.exec(consulta).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Usuario no encontrado')

    if datos_usuario.correo:
        usuario.correo = datos_usuario.correo

    if datos_usuario.id_rol:
        consulta = select(Rol).where(Rol.id == datos_usuario.id_rol)
        rol = session.exec(consulta).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Rol no encontrado")
        usuario.id_rol = datos_usuario.id_rol

    usuario.sqlmodel_update(datos_usuario.model_dump(exclude_unset=True))
    usuario.updated_at = datetime.utcnow()

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
