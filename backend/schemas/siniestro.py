"""
Schemas para Siniestro
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class SiniestroBase(BaseModel):
    """Schema base de siniestro"""
    fecha: Optional[date] = None
    hora: Optional[time] = None
    avenida_id: int
    tipo_id: int
    nivel_gravedad: Optional[str] = None
    victimas_fatales: Optional[int] = 0
    heridos: Optional[int] = 0
    num_vehiculos: Optional[int] = 0
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True  # pydantic v2: reemplaza orm_mode

class SiniestroCreate(SiniestroBase):
    """Schema para crear siniestro"""
    usuario_id: int = Field(..., gt=0)
    
    # NOTA: dia_semana y es_fin_de_semana se calculan automáticamente en el service
    # No es necesario que el usuario los envíe

class SiniestroUpdate(SiniestroBase):
    """Schema para actualizar siniestro"""
    # Permitimos que todos los campos sean opcionales al actualizar
    avenida_id: Optional[int] = None
    tipo_id: Optional[int] = None

class SiniestroOut(SiniestroBase):
    """Schema para respuesta de siniestro"""
    id: int
    # Estos campos adicionales sí existen en la base de datos y se devuelven en las consultas
    dia_semana: Optional[str] = None
    es_fin_de_semana: Optional[bool] = None

# Alias para compatibilidad con cualquier import que espere SiniestroResponse
SiniestroResponse = SiniestroOut