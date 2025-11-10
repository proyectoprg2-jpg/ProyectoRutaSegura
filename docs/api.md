# Configuración

## Variables de entorno del Backend

Editar el archivo `backend/config/settings.py`:
```python
DATABASE_HOST = "localhost"
DATABASE_PORT = 3306
DATABASE_USER = "root"
DATABASE_PASSWORD = "tu_password"
DATABASE_NAME = "siniestros_viales"
```

## Configuración de CORS

El backend está configurado para aceptar peticiones desde:

- http://localhost:5173
- http://127.0.0.1:5173

Para agregar otros orígenes, editar `backend/main.py`:
```python
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://tu-dominio.com"
]
```

## Configuración del Frontend

La URL del API se configura en `frontend/src/services/api.js`:
```javascript
const API_URL = 'http://localhost:8000/api';
