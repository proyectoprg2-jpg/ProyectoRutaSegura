from .auth import (
    Token,
    TokenData,
    LoginRequest,
    RegisterRequest,
    ChangePasswordRequest
)

from .usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioInDB
)

from .avenida import (
    AvenidaBase,
    AvenidaCreate,
    AvenidaUpdate,
    AvenidaResponse
)

from .tipo_siniestro import (
    TipoSiniestroBase,
    TipoSiniestroCreate,
    TipoSiniestroUpdate,
    TipoSiniestroResponse
)

from .siniestro import (
    SiniestroBase,
    SiniestroCreate, 
    SiniestroUpdate,
    SiniestroOut
)

from .vehiculo import (
    VehiculoBase,
    VehiculoCreate,
    VehiculoUpdate,
    VehiculoResponse
)

from .reporte_delito import (
    ReporteDelictivoBase,
    ReporteDelictivoCreate,
    ReporteDelictivoUpdate,
    ReporteDelictivoOut,
    ReporteDelictivoResponse
)

__all__ = [
    "Token",
    "TokenData",
    "LoginRequest",
    "RegisterRequest",
    "ChangePasswordRequest",
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioInDB",
    "AvenidaBase",
    "AvenidaCreate",
    "AvenidaUpdate",
    "AvenidaResponse",
    "TipoSiniestroBase",
    "TipoSiniestroCreate",
    "TipoSiniestroUpdate",
    "TipoSiniestroResponse",
    "SiniestroBase",
    "SiniestroCreate",
    "SiniestroUpdate",
    "SiniestroOut",
    "VehiculoBase",
    "VehiculoCreate",
    "VehiculoUpdate",
    "VehiculoResponse",
    "ReporteDelictivoBase",
    "ReporteDelictivoCreate",
    "ReporteDelictivoUpdate",
    "ReporteDelictivoOut",
    "ReporteDelictivoResponse",
]