from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, time
from decimal import Decimal


class ReporteDelictivoBase(BaseModel):
    latitud: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitud: Optional[Decimal] = Field(None, ge=-180, le=180)
    direccion_aproximada: str = Field(..., min_length=5, max_length=255)
    tipo_delito: str = Field(..., min_length=3, max_length=50)
    descripcion_breve: Optional[str] = Field(None, max_length=500)
    fecha_reporte: date
    hora_aproximada: Optional[time] = None
    nivel_peligrosidad: str = Field(default="media")

    class Config:
        from_attributes = True

    @field_validator('nivel_peligrosidad')
    @classmethod
    def validar_nivel(cls, valor: str) -> str:
        niveles_validos = ['baja', 'media', 'alta']
        valor_lower = valor.lower()
        if valor_lower not in niveles_validos:
            raise ValueError(f"Nivel debe ser: {', '.join(niveles_validos)}")
        return valor_lower


class ReporteDelictivoCreate(ReporteDelictivoBase):
    usuario_id: int = Field(..., gt=0)


class ReporteDelictivoUpdate(ReporteDelictivoBase):
    direccion_aproximada: Optional[str] = Field(None, min_length=5, max_length=255)
    tipo_delito: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_reporte: Optional[date] = None


class ReporteDelictivoOut(ReporteDelictivoBase):
    id: int
    usuario_id: int
    fecha_registro: Optional[str] = None
    ultima_modificacion: Optional[str] = None
    usuario_nombre: Optional[str] = None


ReporteDelictivoResponse = ReporteDelictivoOut