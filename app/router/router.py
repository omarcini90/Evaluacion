from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Body
from app.schemas.list import VerificarPersonaRequest, VerificarPersonaResponse, ErrorResponse
from app.business_logic.list import BlacklistService
from app.repositorio.repository import BlacklistRepository
from app.auth import get_current_user

router = APIRouter()

# @router.on_event("startup")
# def cargar_nombres_iniciales():
#     BlacklistRepository.cargar_nombres_iniciales()

@router.post("/cargar_nombres_iniciales", status_code=status.HTTP_201_CREATED)
async def cargar_nombres_iniciales(list_nombres: List[str] = Body(...)):
    try:
        if not list_nombres:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron nombres")

        BlacklistRepository.cargar_nombres_iniciales(list_nombres)
        return {"message": "Nombres cargados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/verificar",
    response_model=VerificarPersonaResponse,
    responses={
        200: {"model": VerificarPersonaResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Verificar persona en lista negra"
)
def verificar_persona(request: VerificarPersonaRequest, user: dict = Depends(get_current_user)):
    try:
        encontrado = BlacklistService.verificar_persona(request.nombre_completo)
        return VerificarPersonaResponse(encontrado=encontrado)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la conexión a la base de datos")
