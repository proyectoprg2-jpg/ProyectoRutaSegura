from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import logging

from schemas.reporte_delito import ReporteDelictivoCreate, ReporteDelictivoUpdate


async def crear_reporte_delito(db: AsyncSession, reporte: ReporteDelictivoCreate) -> dict:
    """Crea un nuevo reporte de delito en la base de datos"""
    query = text("""
        INSERT INTO reportes_delictivos (
            latitud, longitud, direccion_aproximada, tipo_delito,
            descripcion_breve, fecha_reporte, hora_aproximada,
            nivel_peligrosidad, usuario_id
        ) VALUES (
            :latitud, :longitud, :direccion_aproximada, :tipo_delito,
            :descripcion_breve, :fecha_reporte, :hora_aproximada,
            :nivel_peligrosidad, :usuario_id
        )
    """)
    
    valores = {
        "latitud": reporte.latitud,
        "longitud": reporte.longitud,
        "direccion_aproximada": reporte.direccion_aproximada,
        "tipo_delito": reporte.tipo_delito,
        "descripcion_breve": reporte.descripcion_breve,
        "fecha_reporte": reporte.fecha_reporte,
        "hora_aproximada": reporte.hora_aproximada,
        "nivel_peligrosidad": reporte.nivel_peligrosidad,
        "usuario_id": reporte.usuario_id
    }
    
    result = await db.execute(query, valores)
    await db.commit()
    
    reporte_id = result.lastrowid
    return await obtener_reporte_delito_por_id(db, reporte_id)


async def obtener_reporte_delito_por_id(db: AsyncSession, reporte_id: int) -> Optional[dict]:
    """Obtiene un reporte de delito por su ID con información del usuario"""
    query = text("""
        SELECT 
            r.id, r.latitud, r.longitud, r.direccion_aproximada,
            r.tipo_delito, r.descripcion_breve, r.fecha_reporte,
            r.hora_aproximada, r.nivel_peligrosidad, r.usuario_id,
            r.fecha_registro, r.ultima_modificacion,
            u.nombre as usuario_nombre
        FROM reportes_delictivos r
        INNER JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.id = :id
    """)
    
    result = await db.execute(query, {"id": reporte_id})
    reporte = result.fetchone()
    
    if not reporte:
        return None
    
    return {
        "id": reporte.id,
        "latitud": reporte.latitud,
        "longitud": reporte.longitud,
        "direccion_aproximada": reporte.direccion_aproximada,
        "tipo_delito": reporte.tipo_delito,
        "descripcion_breve": reporte.descripcion_breve,
        "fecha_reporte": reporte.fecha_reporte,
        "hora_aproximada": reporte.hora_aproximada,
        "nivel_peligrosidad": reporte.nivel_peligrosidad,
        "usuario_id": reporte.usuario_id,
        "fecha_registro": reporte.fecha_registro,
        "ultima_modificacion": reporte.ultima_modificacion,
        "usuario_nombre": reporte.usuario_nombre
    }


async def obtener_todos_reportes_delito(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    tipo_delito: Optional[str] = None,
    nivel_peligrosidad: Optional[str] = None
) -> List[dict]:
    """Obtiene lista de reportes de delitos con filtros opcionales"""
    where_clauses = []
    valores = {"skip": skip, "limit": limit}
    
    if tipo_delito:
        where_clauses.append("r.tipo_delito = :tipo_delito")
        valores["tipo_delito"] = tipo_delito
    
    if nivel_peligrosidad:
        where_clauses.append("r.nivel_peligrosidad = :nivel_peligrosidad")
        valores["nivel_peligrosidad"] = nivel_peligrosidad
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    query = text(f"""
        SELECT 
            r.id, r.latitud, r.longitud, r.direccion_aproximada,
            r.tipo_delito, r.descripcion_breve, r.fecha_reporte,
            r.hora_aproximada, r.nivel_peligrosidad, r.usuario_id,
            r.fecha_registro, r.ultima_modificacion,
            u.nombre as usuario_nombre
        FROM reportes_delictivos r
        INNER JOIN usuarios u ON r.usuario_id = u.id
        {where_sql}
        ORDER BY r.fecha_reporte DESC, r.fecha_registro DESC
        LIMIT :limit OFFSET :skip
    """)
    
    result = await db.execute(query, valores)
    reportes = result.fetchall()
    
    return [
        {
            "id": r.id,
            "latitud": r.latitud,
            "longitud": r.longitud,
            "direccion_aproximada": r.direccion_aproximada,
            "tipo_delito": r.tipo_delito,
            "descripcion_breve": r.descripcion_breve,
            "fecha_reporte": r.fecha_reporte,
            "hora_aproximada": r.hora_aproximada,
            "nivel_peligrosidad": r.nivel_peligrosidad,
            "usuario_id": r.usuario_id,
            "fecha_registro": r.fecha_registro,
            "ultima_modificacion": r.ultima_modificacion,
            "usuario_nombre": r.usuario_nombre
        }
        for r in reportes
    ]


async def actualizar_reporte_delito(
    db: AsyncSession,
    reporte_id: int,
    reporte_update: ReporteDelictivoUpdate
) -> Optional[dict]:
    """Actualiza un reporte de delito existente"""
    campos_actualizar = []
    valores = {"id": reporte_id}
    
    if reporte_update.latitud is not None:
        campos_actualizar.append("latitud = :latitud")
        valores["latitud"] = reporte_update.latitud
    
    if reporte_update.longitud is not None:
        campos_actualizar.append("longitud = :longitud")
        valores["longitud"] = reporte_update.longitud
    
    if reporte_update.direccion_aproximada is not None:
        campos_actualizar.append("direccion_aproximada = :direccion_aproximada")
        valores["direccion_aproximada"] = reporte_update.direccion_aproximada
    
    if reporte_update.tipo_delito is not None:
        campos_actualizar.append("tipo_delito = :tipo_delito")
        valores["tipo_delito"] = reporte_update.tipo_delito
    
    if reporte_update.descripcion_breve is not None:
        campos_actualizar.append("descripcion_breve = :descripcion_breve")
        valores["descripcion_breve"] = reporte_update.descripcion_breve
    
    if reporte_update.fecha_reporte is not None:
        campos_actualizar.append("fecha_reporte = :fecha_reporte")
        valores["fecha_reporte"] = reporte_update.fecha_reporte
    
    if reporte_update.hora_aproximada is not None:
        campos_actualizar.append("hora_aproximada = :hora_aproximada")
        valores["hora_aproximada"] = reporte_update.hora_aproximada
    
    if reporte_update.nivel_peligrosidad is not None:
        campos_actualizar.append("nivel_peligrosidad = :nivel_peligrosidad")
        valores["nivel_peligrosidad"] = reporte_update.nivel_peligrosidad
    
    if not campos_actualizar:
        return await obtener_reporte_delito_por_id(db, reporte_id)
    
    query = text(f"""
        UPDATE reportes_delictivos
        SET {', '.join(campos_actualizar)}
        WHERE id = :id
    """)
    
    await db.execute(query, valores)
    await db.commit()
    
    return await obtener_reporte_delito_por_id(db, reporte_id)


async def eliminar_reporte_delito(
    db: AsyncSession,
    reporte_id: int,
    usuario_id: int,
    es_admin: bool = False
) -> bool:
    """Elimina un reporte de delito verificando permisos"""
    try:
        query_verificar = text("""
            SELECT usuario_id FROM reportes_delictivos WHERE id = :reporte_id
        """)
        result = await db.execute(query_verificar, {"reporte_id": reporte_id})
        reporte = result.fetchone()
        
        if not reporte:
            return False
        
        if not es_admin and reporte.usuario_id != usuario_id:
            raise PermissionError("No tienes permiso para eliminar este reporte")
        
        query_eliminar = text("DELETE FROM reportes_delictivos WHERE id = :reporte_id")
        await db.execute(query_eliminar, {"reporte_id": reporte_id})
        await db.commit()
        
        return True
    
    except PermissionError:
        raise
    except Exception as e:
        await db.rollback()
        logging.error(f"Error al eliminar reporte {reporte_id}: {str(e)}")
        return False


async def contar_reportes_delito(
    db: AsyncSession,
    tipo_delito: Optional[str] = None,
    nivel_peligrosidad: Optional[str] = None
) -> int:
    """Cuenta total de reportes de delitos con filtros opcionales"""
    where_clauses = []
    valores = {}
    
    if tipo_delito:
        where_clauses.append("tipo_delito = :tipo_delito")
        valores["tipo_delito"] = tipo_delito
    
    if nivel_peligrosidad:
        where_clauses.append("nivel_peligrosidad = :nivel_peligrosidad")
        valores["nivel_peligrosidad"] = nivel_peligrosidad
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    
    query = text(f"""
        SELECT COUNT(*) as total
        FROM reportes_delictivos
        {where_sql}
    """)
    
    result = await db.execute(query, valores)
    row = result.fetchone()
    
    return row.total if row else 0


async def obtener_estadisticas_delitos(db: AsyncSession) -> dict:
    """Obtiene estadísticas generales de reportes de delitos"""
    query = text("""
        SELECT 
            COUNT(*) as total_reportes,
            COUNT(CASE WHEN nivel_peligrosidad = 'alta' THEN 1 END) as delitos_alta_peligrosidad,
            COUNT(CASE WHEN nivel_peligrosidad = 'media' THEN 1 END) as delitos_media_peligrosidad,
            COUNT(CASE WHEN nivel_peligrosidad = 'baja' THEN 1 END) as delitos_baja_peligrosidad
        FROM reportes_delictivos
    """)
    
    result = await db.execute(query)
    row = result.fetchone()
    
    if not row:
        return {}
    
    return {
        "total_reportes": row.total_reportes,
        "delitos_alta_peligrosidad": row.delitos_alta_peligrosidad,
        "delitos_media_peligrosidad": row.delitos_media_peligrosidad,
        "delitos_baja_peligrosidad": row.delitos_baja_peligrosidad
    }


async def obtener_delitos_por_tipo(db: AsyncSession) -> List[dict]:
    """Obtiene cantidad de delitos agrupados por tipo"""
    query = text("""
        SELECT 
            tipo_delito,
            COUNT(*) as cantidad,
            COUNT(CASE WHEN nivel_peligrosidad = 'alta' THEN 1 END) as cantidad_alta,
            COUNT(CASE WHEN nivel_peligrosidad = 'media' THEN 1 END) as cantidad_media,
            COUNT(CASE WHEN nivel_peligrosidad = 'baja' THEN 1 END) as cantidad_baja
        FROM reportes_delictivos
        GROUP BY tipo_delito
        ORDER BY cantidad DESC
    """)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return [
        {
            "tipo_delito": r.tipo_delito,
            "cantidad": r.cantidad,
            "cantidad_alta": r.cantidad_alta,
            "cantidad_media": r.cantidad_media,
            "cantidad_baja": r.cantidad_baja
        }
        for r in rows
    ]


async def obtener_zonas_peligrosas(db: AsyncSession, limite: int = 10) -> List[dict]:
    """Obtiene las zonas con más reportes de delitos"""
    query = text("""
        SELECT 
            direccion_aproximada,
            COUNT(*) as total_delitos,
            COUNT(CASE WHEN nivel_peligrosidad = 'alta' THEN 1 END) as delitos_graves,
            GROUP_CONCAT(DISTINCT tipo_delito SEPARATOR ', ') as tipos_delito
        FROM reportes_delictivos
        GROUP BY direccion_aproximada
        ORDER BY total_delitos DESC, delitos_graves DESC
        LIMIT :limite
    """)
    
    result = await db.execute(query, {"limite": limite})
    rows = result.fetchall()
    
    return [
        {
            "direccion": r.direccion_aproximada,
            "total_delitos": r.total_delitos,
            "delitos_graves": r.delitos_graves,
            "tipos_delito": r.tipos_delito
        }
        for r in rows
    ]