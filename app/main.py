from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.router.router import router as verification_router


# Crear la aplicación FastAPI
import yaml
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import FileResponse, HTMLResponse
import os

# Cargar el OpenAPI YAML externo
OPENAPI_YAML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "openapi.yaml")
with open(OPENAPI_YAML_PATH, "r", encoding="utf-8") as f:
    openapi_spec = yaml.safe_load(f)

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sobrescribir el esquema OpenAPI con el YAML externo
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    return openapi_spec

# Swagger UI personalizado
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Documentación - Microservicio de Verificación de Lista Negra"
    )

# Redoc personalizado
@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Documentación Redoc - Microservicio de Verificación de Lista Negra"
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
