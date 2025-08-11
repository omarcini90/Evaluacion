from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.router.router import router as verification_router


# Crear la aplicación FastAPI
app = FastAPI(
    title="Microservicio de Verificación de Lista Negra",
    description="""
    Microservicio REST para verificar si una persona se encuentra en una lista negra.
    
    ## Características
    
    * **Autenticación JWT**: Todas las operaciones requieren autenticación Bearer Token
    * **Verificación de personas**: Consulta si una persona está en la lista negra
    * **Base de datos PostgreSQL**: Almacenamiento persistente de la lista negra
    * **Documentación automática**: OpenAPI/Swagger integrado
    
    ## Autenticación
    
    Para usar este API, necesitas incluir un token JWT en el header:
    ```
    Authorization: Bearer tu_token_aqui
    ```
    
    Para pruebas, puedes usar este token hardcodeado:
    ```
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjk5OTk5OTk5OTl9.Jz8n5r7Y5oU8i6A2cX4l8N3vB9u1K6t3R7yW5qE8zF2
    ```
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "dev@empresa.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(verification_router)

# Handler global para excepciones no manejadas
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# Endpoint de health check
@app.get("/health", tags=["health"])
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    return {"status": "healthy", "service": "blacklist-verification"}

# Endpoint de información
@app.get("/", tags=["info"])
async def root():
    """Información básica del servicio"""
    return {
        "message": "Microservicio de Verificación de Lista Negra",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
