# API Endpoints

## Autenticación

### Login
- POST /api/auth/login
- Body: { email, password }
- Respuesta: { token, user }

## Siniestros

### Listar siniestros
- GET /api/siniestros
- Query params: skip, limit, avenida_id, tipo_id, nivel_gravedad

### Crear siniestro
- POST /api/siniestros
- Body: SiniestroCreate

### Obtener siniestro
- GET /api/siniestros/{id}

### Actualizar siniestro
- PUT /api/siniestros/{id}
- Body: SiniestroUpdate

### Eliminar siniestro
- DELETE /api/siniestros/{id}

## Reportes Delictivos

### Listar reportes
- GET /api/reportes-delito
- Query params: skip, limit, tipo_delito

### Crear reporte
- POST /api/reportes-delito
- Body: ReporteDelitoCreate

### Obtener reporte
- GET /api/reportes-delito/{id}

### Actualizar reporte
- PUT /api/reportes-delito/{id}
- Body: ReporteDelitoUpdate

### Eliminar reporte
- DELETE /api/reportes-delito/{id}

## Análisis

### Índice de seguridad
- GET /api/reportes/analisis/indice-seguridad
- Respuesta: Lista de avenidas con índice calculado

### Rutas seguras
- GET /api/reportes/analisis/rutas-seguras
- Query params: limit
- Respuesta: Top rutas más seguras

### Zonas peligrosas
- GET /api/reportes/analisis/zonas-peligrosas
- Query params: limit
- Respuesta: Top zonas más peligrosas

## Reportes Estadísticos

### Siniestros por zona
- GET /api/reportes/siniestros-zona

### Avenidas peligrosas
- GET /api/reportes/avenidas-peligrosas

### Estadísticas por tipo
- GET /api/reportes/estadisticas-tipo

### Resumen general
- GET /api/reportes/resumen