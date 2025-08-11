from pydantic import BaseModel, Field

class VerificarPersonaRequest(BaseModel):
    nombre_completo: str = Field(..., min_length=1, description="Nombre completo de la persona a verificar")

class VerificarPersonaResponse(BaseModel):
    encontrado: bool = Field(..., description="Indica si la persona está en la lista negra")

class ErrorResponse(BaseModel):
    detail: str
