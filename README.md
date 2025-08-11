# Microservicio de Verificación de Personas en Lista Negra

Este microservicio permite verificar si una persona está en una lista negra almacenada en PostgreSQL. Está construido con FastAPI y utiliza autenticación JWT.

## Instalación rápida

1. Clona el repositorio y entra al directorio:
   ```bash
   git clone <repo-url>
   cd Evaluacion
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea la base de datos y la tabla (ver más abajo).
4. Ejecuta la app:
   ```bash
   uvicorn app.main:app --reload
   ```

## Variables de entorno

- `DATABASE_URL` (opcional, por defecto usa postgres local)
- `JWT_SECRET_KEY` (clave para firmar JWT)

## Endpoints principales

### POST /verificar
Verifica si una persona está en la lista negra.

**Headers:**
- Authorization: Bearer <token>
- Content-Type: application/json

**Body:**
```json
{
  "nombre_completo": "Juan Pérez González"
}
```

**Respuesta:**
```json
{
  "encontrado": true
}
```

### POST /cargar_nombres_iniciales
Carga una lista de nombres en la lista negra (batch).

**Body:**
```json
[
  "Juan Pérez González",
  "María García López",
  "Carlos Rodríguez Martín",
  "Ana Fernández Ruiz",
  "Luis Martínez Sánchez",
  "Carmen Jiménez Torres",
  "Francisco Moreno Díaz",
  "Isabel Álvarez Romero",
  "Pedro Gómez Navarro",
  "Lucía Herrera Castro"
]
```

**Ejemplo cURL:**
```bash
curl -X POST "http://localhost:8000/cargar_nombres_iniciales" \
     -H "Content-Type: application/json" \
     -d '["Juan Pérez González","María García López","Carlos Rodríguez Martín","Ana Fernández Ruiz","Luis Martínez Sánchez","Carmen Jiménez Torres","Francisco Moreno Díaz","Isabel Álvarez Romero","Pedro Gómez Navarro","Lucía Herrera Castro"]'
```

**Respuesta:**
```json
{
  "message": "Nombres cargados exitosamente"
}
```

### Otros endpoints
- `GET /health`: Health check
- `GET /`: Información básica

## Autenticación

Todos los endpoints protegidos requieren un JWT válido. Para pruebas puedes usar este token:
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjk5OTk5OTk5OTl9.Jz8n5r7Y5oU8i6A2cX4l8N3vB9u1K6t3R7yW5qE8zF2
```

## Script para crear la tabla

```sql
CREATE TABLE IF NOT EXISTS personas_bloqueadas (
    id SERIAL PRIMARY KEY,
    nombre_completo TEXT UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Notas
- El endpoint de carga de nombres es útil para inicializar la base o hacer pruebas.
- Si tienes dudas, revisa el código fuente, es sencillo y está comentado.
