# RutaSegura - Sistema de Análisis de Seguridad Vial

Proyecto universitario para la cátedra de Programación 2.
Sistema web para el análisis integral de seguridad en rutas de La Rioja, considerando tanto siniestros viales como reportes delictivos.

## Descripción

RutaSegura es una plataforma que permite registrar y analizar siniestros de tránsito y reportes de delitos para determinar un índice de seguridad por zona. El objetivo es proporcionar información útil para la toma de decisiones en materia de seguridad vial y urbana.

## Funcionalidades Principales

- Gestión de siniestros viales con datos detallados
- Registro de reportes delictivos georreferenciados
- Cálculo de índice de seguridad por avenida
- Análisis estadístico con gráficos
- Sistema de autenticación con roles
- Reportes y consultas avanzadas con INNER JOIN, GROUP BY y subconsultas

## Tecnologías Utilizadas

### Backend
- Python 3.10+
- FastAPI (Framework web asíncrono)
- SQLAlchemy (ORM con soporte asíncrono)
- MySQL (Base de datos)
- Pydantic (Validación de datos)
- bcrypt (Hash de contraseñas)
- Pandas (Análisis de datos)

### Frontend
- React 18
- Vite (Build tool)
- React Router (Navegación)
- Axios (HTTP client)
- Recharts (Gráficos)
- Lucide React (Iconos)
- Tailwind CSS (Estilos)

## Estructura del Proyecto
```
RutaSegura/
├── backend/
│   ├── config/          # Configuración de BD y settings
│   ├── database/        # Scripts de importación y CSVs
│   ├── routers/         # Endpoints de la API
│   ├── services/        # Lógica de negocio
│   ├── schemas/         # Validación con Pydantic
│   ├── analysis/        # Scripts de análisis de datos
│   └── main.py          # Aplicación principal
├── frontend/
│   ├── src/
│   │   ├── components/  # Componentes reutilizables
│   │   ├── pages/       # Páginas principales
│   │   ├── services/    # Cliente API
│   │   └── context/     # Context API de React
│   └── public/
└── README.md
```

## Instalación y Configuración

### Requisitos Previos

- Python 3.10 o superior
- Node.js 16 o superior
- MySQL 8.0 o superior
- Git

### Configuración del Backend

1. Crear base de datos en MySQL:
```sql
CREATE DATABASE siniestros_viales CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Ejecutar el script de creación de tablas (schema.sql en el directorio database/)

3. Navegar al directorio backend:
```bash
cd backend
```

4. Crear y activar entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

5. Instalar dependencias:
```bash
pip install -r requirements.txt
```

6. Configurar variables de entorno en `backend/config/settings.py`:
```python
DATABASE_HOST = "localhost"
DATABASE_PORT = 3306
DATABASE_USER = "root"
DATABASE_PASSWORD = "tu_password"
DATABASE_NAME = "siniestros_viales"
```

7. Importar datos iniciales:
```bash
cd database
python import_data.py
```

8. Iniciar servidor:
```bash
cd ..
uvicorn main:app --reload
```

El backend estará disponible en http://localhost:8000

### Configuración del Frontend

1. Navegar al directorio frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Iniciar servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en http://localhost:5173

## Uso del Sistema

### Credenciales de Acceso

Después de importar los datos, se crean estos usuarios por defecto:

- Administrador:
  - Email: admin@rutasegura.com
  - Password: admin123

- Editor:
  - Email: editor@rutasegura.com
  - Password: editor123

- Consultor:
  - Email: consultor@rutasegura.com
  - Password: consultor123

### Endpoints Principales

#### Siniestros
- GET /api/siniestros - Listar siniestros
- POST /api/siniestros - Crear siniestro
- PUT /api/siniestros/{id} - Actualizar siniestro
- DELETE /api/siniestros/{id} - Eliminar siniestro

#### Reportes Delictivos
- GET /api/reportes-delito - Listar reportes
- POST /api/reportes-delito - Crear reporte
- PUT /api/reportes-delito/{id} - Actualizar reporte
- DELETE /api/reportes-delito/{id} - Eliminar reporte

#### Análisis
- GET /api/reportes/analisis/indice-seguridad - Índice de seguridad por avenida
- GET /api/reportes/analisis/rutas-seguras - Top rutas más seguras
- GET /api/reportes/analisis/zonas-peligrosas - Top zonas más peligrosas

Documentación completa en: http://localhost:8000/docs

## Algoritmo de Índice de Seguridad

El sistema calcula un índice de peligrosidad para cada avenida usando la siguiente fórmula:
```
Índice Base = (Peso_Siniestros × Total_Siniestros) + (Peso_Delitos × Total_Delitos)

Donde:
- Peso_Siniestros = 3.0
- Peso_Delitos = 2.0

Si hay víctimas fatales:
Índice Final = Índice Base × 1.5
```

### Clasificación de Seguridad

- 0: Muy Segura
- 1-10: Segura
- 11-25: Moderada
- 26-50: Peligrosa
- Mayor a 50: Muy Peligrosa

## Características Técnicas

### Programación Orientada a Objetos

El proyecto implementa POO a través de:
- Schemas de Pydantic para validación de datos
- Servicios organizados por responsabilidad única
- Separación clara de capas (routers, services, database)

### Consultas SQL Avanzadas

El sistema incluye ejemplos de:
- INNER JOIN para relacionar múltiples tablas
- GROUP BY con agregaciones (COUNT, SUM, AVG)
- Subconsultas correlacionadas
- Funciones de ventana para análisis temporal

### Análisis de Datos

Uso de Pandas para:
- Importación de datos desde CSV
- Limpieza y transformación de datos
- Análisis exploratorio de datos (EDA)
- Generación de estadísticas descriptivas

## Dependencias del Backend
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
aiomysql==0.2.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
bcrypt==4.1.1
pandas==2.1.3
mysql-connector-python==8.2.0
```

## Dependencias del Frontend
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2",
  "recharts": "^2.10.3",
  "lucide-react": "^0.294.0"
}
```

## Autores

Proyecto desarrollado para la cátedra de Programación 2.
Universidad - La Rioja, Argentina.

## Notas de Desarrollo

- El proyecto usa arquitectura de tres capas (Presentación, Lógica de Negocio, Datos)
- Las consultas SQL están optimizadas con índices en campos de búsqueda frecuente
- El frontend implementa Context API para manejo de estado global
- La autenticación usa tokens que se almacenan en localStorage
- Los datos de ejemplo están en formato CSV con separador punto y coma

## Problemas Conocidos

- La georreferenciación de delitos con avenidas es aproximada
- No hay paginación en todas las consultas
- El sistema no valida duplicados en la carga de datos

## Mejoras Futuras

- Implementar paginación completa
- Agregar mapas interactivos con Leaflet o Google Maps
- Sistema de notificaciones en tiempo real
- Exportación de reportes a PDF
- API REST completa con autenticación JWT

