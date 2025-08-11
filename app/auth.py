from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config.config import settings

# Esquema de seguridad Bearer
security = HTTPBearer()

class JWTAuthenticationService:
    """Servicio para autenticación JWT"""
    
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.valid_test_token = settings.valid_test_token
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        """
        Verifica la validez del token JWT
        
        Args:
            credentials: Credenciales del header Authorization
            
        Returns:
            dict: Payload del token decodificado
            
        Raises:
            HTTPException: Si el token es inválido o ha expirado
        """
        token = credentials.credentials
        
        # Para propósitos de demostración, también aceptamos el token hardcodeado
        if token == self.valid_test_token:
            return {"sub": "test_user", "valid": True}
        
        try:
            # Decodificar el token JWT
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido: no se encontró el usuario",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return payload
            
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Instancia global del servicio de autenticación
auth_service = JWTAuthenticationService()

def get_current_user(token_data: dict = Depends(auth_service.verify_token)) -> dict:
    """
    Dependency para obtener el usuario actual desde el token
    
    Args:
        token_data: Datos del token decodificado
        
    Returns:
        dict: Información del usuario
    """
    return token_data
