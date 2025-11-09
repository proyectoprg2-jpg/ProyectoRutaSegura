# Backend

## Estructura
```
backend/
├── config/          # Configuración
├── routers/         # Endpoints API
├── services/        # Lógica de negocio
├── schemas/         # Validación Pydantic
└── database/        # Scripts e importación
```

## Arquitectura

El backend sigue una arquitectura en capas:

1. Routers: Reciben peticiones HTTP
2. Services: Procesan lógica de negocio
3. Database: Acceso a datos

## Servicios principales

### services/siniestros.py
Gestión de siniestros viales:
- CRUD completo
- Filtros avanzados
- Verificación de permisos

### services/reportes_delito.py
Gestión de reportes delictivos:
- CRUD completo
- Filtros por tipo
- Conteo de reportes

### services/reportes.py
Análisis y reportes:
- Índice de seguridad
- Rutas seguras
- Zonas peligrosas
- Estadísticas

## Consultas SQL avanzadas

El sistema incluye:
- INNER JOIN para relacionar tablas
- GROUP BY con agregaciones
- Subconsultas correlacionadas
- Funciones de ventana

## Seguridad

- Autenticación con bcrypt
- Hash de contraseñas
- Validación de permisos por rol
- Sanitización de inputs con Pydantic