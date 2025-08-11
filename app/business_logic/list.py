from app.repositorio.repository import BlacklistRepository

class BlacklistService:
    """Lógica de negocio para verificación de lista negra."""
    @staticmethod
    def verificar_persona(nombre_completo: str) -> bool:
        if not nombre_completo or not nombre_completo.strip():
            raise ValueError("El nombre completo no puede estar vacío")
        nombre_normalizado = " ".join(nombre_completo.strip().split())
        if len(nombre_normalizado) < 2:
            raise ValueError("El nombre completo debe tener al menos 2 caracteres")
        return BlacklistRepository.persona_bloqueada(nombre_normalizado)
