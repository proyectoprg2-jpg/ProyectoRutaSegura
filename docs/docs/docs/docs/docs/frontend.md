# Frontend

## Estructura
```
frontend/
├── src/
│   ├── pages/          # Páginas principales
│   ├── components/     # Componentes reutilizables
│   ├── services/       # Cliente API
│   ├── context/        # Estado global
│   └── assets/         # Recursos estáticos
```

## Páginas principales

- Dashboard: Estadísticas generales
- Siniestros: Gestión de siniestros
- Reportes: Análisis estadísticos
- Zonas Peligrosas: Reportes delictivos
- Análisis Ruta Segura: Índice de seguridad
- Usuarios: Gestión de usuarios (admin)

## Componentes clave

### Layout
Componente principal que envuelve todas las páginas. Incluye:
- Sidebar de navegación
- Header con usuario
- Área de contenido

### AuthContext
Context API para manejo de autenticación:
- Login/Logout
- Información del usuario
- Verificación de roles

## Rutas
```javascript
/ - Dashboard
/siniestros - Gestión de siniestros
/reportes - Reportes estadísticos
/zonas-peligrosas - Reportes delictivos
/analisis-ruta-segura - Índice de seguridad
/usuarios - Gestión de usuarios (admin)
```

## Tecnologías

- React 18
- React Router 6
- Axios
- Recharts
- Tailwind CSS
- Lucide React