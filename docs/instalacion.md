# Instalación

## Requisitos previos

- Python 3.10 o superior
- Node.js 16 o superior
- MySQL 8.0 o superior
- Git

## Instalación del Backend

### 1. Crear base de datos

Ejecutar en MySQL:
```sql
CREATE DATABASE siniestros_viales CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configurar entorno virtual
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Importar datos iniciales
```bash
cd database
python import_data.py
```

### 5. Iniciar servidor
```bash
cd ..
uvicorn main:app --reload
```

El backend estará en http://localhost:8000

## Instalación del Frontend

### 1. Instalar dependencias
```bash
cd frontend
npm install
```

### 2. Iniciar servidor de desarrollo
```bash
npm run dev
```

El frontend estará en http://localhost:5173

## Credenciales por defecto

Después de importar los datos:

- Admin: admin@rutasegura.com / admin123
- Editor: editor@rutasegura.com / editor123
- Consultor: consultor@rutasegura.com / consultor123