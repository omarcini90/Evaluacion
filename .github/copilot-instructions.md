<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Microservicio de Verificación de Lista Negra - Instrucciones para Copilot

Este es un microservicio REST desarrollado en Python usando FastAPI para verificar personas en una lista negra.

## Arquitectura del Proyecto

- **Patrón Repository**: Usado para abstraer el acceso a datos
- **Patrón Service**: Para la lógica de negocio
- **Inyección de dependencias**: FastAPI Depends para gestionar dependencias
- **Autenticación JWT**: Bearer token authentication
- **Base de datos**: PostgreSQL con SQLAlchemy ORM

## Estructura de Capas

1. **Routers** (`app/routers.py`): Controladores HTTP/REST endpoints
2. **Services** (`app/services.py`): Lógica de negocio y validaciones
3. **Repositories** (`app/repositories.py`): Acceso a datos y consultas DB
4. **Models** (`app/models.py`): Modelos SQLAlchemy de base de datos
5. **Schemas** (`app/schemas.py`): Validación de entrada/salida con Pydantic
6. **Auth** (`app/auth.py`): Servicios de autenticación JWT

## Convenciones de Código

- Usar interfaces/ABC para definir contratos
- Manejar excepciones específicas en cada capa
- Documentar funciones con docstrings tipo Google
- Seguir principios SOLID
- Usar type hints en todas las funciones
- Nombres de clases en PascalCase
- Nombres de funciones y variables en snake_case

## Base de Datos

- Tabla: `personas_bloqueadas`
- Campos: `id`, `nombre_completo`, `fecha_creacion`
- Búsquedas case-insensitive con `ilike()`

## Respuestas HTTP

- 200: Operación exitosa
- 400: Datos malformados
- 401: No autorizado (JWT inválido)
- 500: Error interno (BD, etc.)

Siempre usar los schemas definidos para las respuestas.
