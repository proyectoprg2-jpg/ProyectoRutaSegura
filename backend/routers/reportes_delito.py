from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.database import get_db
from schemas.reporte_delito import ReporteDelitoCreate, ReporteDelitoUpdate, ReporteDelitoResponse
from services.reportes_delito import (
    crear_reporte_delito,
    obtener_reporte_delito_por_id,
    obtener_todos_reportes_delito,
    actualizar_reporte_delito,
    eliminar_reporte_delito,
    contar_reportes_delito
)

router = APIRouter(
    prefix="/api/reportes-delito",
    tags=["Reportes Delictivos"]
)

@router.post("/", response_model=ReporteDelitoResponse)
async def crear_reporte(
    reporte: ReporteDelitoCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crear_reporte_delito(db, reporte)

@router.get("/{reporte_id}", response_model=ReporteDelitoResponse)
async def obtener_reporte(
    reporte_id: int,
    db: AsyncSession = Depends(get_db)
):
    reporte = await obtener_reporte_delito_por_id(db, reporte_id)
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte

@router.get("/", response_model=List[ReporteDelitoResponse])
async def listar_reportes(
    skip: int = 0,
    limit: int = 100,
    tipo_delito: str = None,
    db: AsyncSession = Depends(get_db)
):
    return await obtener_todos_reportes_delito(db, skip, limit, tipo_delito)

@router.put("/{reporte_id}", response_model=ReporteDelitoResponse)
async def actualizar_reporte(
    reporte_id: int,
    reporte: ReporteDelitoUpdate,
    db: AsyncSession = Depends(get_db)
):
    reporte_actualizado = await actualizar_reporte_delito(db, reporte_id, reporte)
    if not reporte_actualizado:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte_actualizado

@router.delete("/{reporte_id}")
async def eliminar_reporte(
    reporte_id: int,
    db: AsyncSession = Depends(get_db)
):
    eliminado = await eliminar_reporte_delito(db, reporte_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"mensaje": "Reporte eliminado correctamente"}

@router.get("/estadisticas/total")
async def obtener_total_reportes(
    tipo_delito: str = None,
    db: AsyncSession = Depends(get_db)
):
    total = await contar_reportes_delito(db, tipo_delito)
    return {"total": total}
