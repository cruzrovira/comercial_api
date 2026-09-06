from typing import Literal

from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.categoria import Categoria
from models.producto import Producto, ProductoCreate, ProductoUpdate, ProductoUpdatePatch
from datetime import datetime

router = APIRouter()


@router.get("/productos", response_model=list[Producto], status_code=status.HTTP_200_OK)
def get_productos(session: SessionDeDependencia,
                  offset: int = Query(
                      0, ge=0),
                  limit: int = Query(
                      100, ge=1,
                  )):
    consulta = select(Producto).offset(offset).limit(limit)
    resultado_de_consulta = session.exec(consulta)
    return resultado_de_consulta.all()


@router.get("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
def get_producto(id: int, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Producto no encontrado")
    return resultado_de_consulta


@router.post('/productos', response_model=Producto, status_code=status.HTTP_201_CREATED)
def create_producto(datos_producto: ProductoCreate, session: SessionDeDependencia):

    consulta = select(Categoria).where(
        Categoria.id == datos_producto.id_categoria)
    categoria = session.exec(consulta).first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Categoria con id {datos_producto.id_categoria} no encontrada")

    producto_nuevo = Producto(
        nombre=datos_producto.nombre,
        descripcion=datos_producto.descripcion,
        precio_compra=datos_producto.precio_compra,
        precio_venta=datos_producto.precio_venta,
        stock=datos_producto.stock,
        imagen=datos_producto.imagen,
        id_categoria=categoria.id
    )
    session.add(producto_nuevo)
    session.commit()
    session.refresh(producto_nuevo)
    return producto_nuevo


@router.delete('/productos/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(id: int, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()
    if not resultado_de_consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Producto no encontrado")
    session.delete(resultado_de_consulta)
    session.commit()
    return None


@router.put('/productos/{id}', response_model=Producto, status_code=status.HTTP_200_OK)
def update_producto(id: int, datos_producto: ProductoUpdate, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Producto no encontrado')

    categoria = session.exec(select(Categoria).where(
        Categoria.id == datos_producto.id_categoria)).first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Categoria con id: {datos_producto.id_categoria} no encontrada , no se puede actualizar el producto")

    if datos_producto.descripcion:
        producto.descripcion = datos_producto.descripcion

    producto.nombre = datos_producto.nombre
    producto.precio_compra = datos_producto.precio_compra
    producto.precio_venta = datos_producto.precio_venta
    producto.stock = datos_producto.stock
    producto.imagen = datos_producto.imagen
    producto.id_categoria = datos_producto.id_categoria
    producto.updated_at = datetime.utcnow()

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.patch('/productos/{id}', response_model=Producto, status_code=status.HTTP_200_OK)
def patch_producto(id: int, datos_producto: ProductoUpdatePatch, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Producto no encontrado')

    if datos_producto.id_categoria:
        categoria = session.exec(select(Categoria).where(
            Categoria.id == datos_producto.id_categoria)).first()

        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Categoria con id: {datos_producto.id_categoria} no encontrada , no se puede actualizar el producto")
        producto.id_categoria = datos_producto.id_categoria

    # Actualiza solo los campos proporcionados en el patch
    producto.sqlmodel_update(datos_producto.model_dump(exclude_unset=True))

    producto.updated_at = datetime.utcnow()

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
