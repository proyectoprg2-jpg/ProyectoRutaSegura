# Base de Datos

## Estructura

### Tabla: usuarios
Gestión de usuarios del sistema
```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('admin', 'editor', 'consultor') DEFAULT 'consultor',
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: avenidas
Catálogo de avenidas de La Rioja
```sql
CREATE TABLE avenidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(50),
    zona VARCHAR(100),
    longitud_km DECIMAL(5,2)
);
```

### Tabla: tipos_siniestro
Catálogo de tipos de siniestros
```sql
CREATE TABLE tipos_siniestro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gravedad ENUM('baja', 'media', 'alta') DEFAULT 'media',
    descripcion TEXT
);
```

### Tabla: siniestros
Registro de siniestros viales
```sql
CREATE TABLE siniestros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    avenida_id INT NOT NULL,
    tipo_id INT NOT NULL,
    nivel_gravedad ENUM('baja', 'media', 'alta') DEFAULT 'media',
    victimas_fatales INT DEFAULT 0,
    heridos INT DEFAULT 0,
    num_vehiculos INT DEFAULT 1,
    dia_semana VARCHAR(20),
    es_fin_de_semana BOOLEAN DEFAULT FALSE,
    usuario_id INT NOT NULL,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (avenida_id) REFERENCES avenidas(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_siniestro(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

### Tabla: vehiculos_involucrados
Vehículos involucrados en siniestros
```sql
CREATE TABLE vehiculos_involucrados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    siniestro_id INT NOT NULL,
    tipo_vehiculo VARCHAR(50),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    rol VARCHAR(50),
    es_fallecido BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (siniestro_id) REFERENCES siniestros(id) ON DELETE CASCADE
);
```

### Tabla: reportes_delictivos
Reportes de delitos georreferenciados
```sql
CREATE TABLE reportes_delictivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitud DECIMAL(10, 6) NOT NULL,
    longitud DECIMAL(10, 6) NOT NULL,
    tipo_delito VARCHAR(50) NOT NULL,
    descripcion_breve TEXT,
    fecha_reporte DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Índice de Seguridad

Fórmula de cálculo:
```
Índice Base = (3 × Total_Siniestros) + (2 × Total_Delitos)

Si hay víctimas fatales:
Índice Final = Índice Base × 1.5
```

Clasificación:
- 0: Muy Segura
- 1-10: Segura
- 11-25: Moderada
- 26-50: Peligrosa
- Mayor a 50: Muy Peligrosa