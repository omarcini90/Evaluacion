from app.config.config import get_connection
from typing import Optional, List

class BlacklistRepository:
    """Repositorio para operaciones sobre la tabla personas_bloqueadas."""

    @staticmethod
    def persona_bloqueada(nombre_completo: str) -> bool:
        """Verifica si una persona está en la lista negra (case-insensitive)."""
        query = """
            SELECT 1 FROM personas_bloqueadas WHERE LOWER(nombre_completo) = LOWER(%s) LIMIT 1;
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (nombre_completo.strip(),))
                    return cur.fetchone() is not None
        except Exception as e:
            raise Exception(f"Error al consultar la base de datos: {str(e)}")

    @staticmethod
    def cargar_nombres_iniciales(nombres: List[str]):
        """Carga una lista de nombres bloqueados si la tabla está vacía o para agregar más."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) AS total FROM personas_bloqueadas;")
                    count = cur.fetchone()["total"]
                    if count == 0:
                        for nombre in nombres:
                            cur.execute(
                                "INSERT INTO personas_bloqueadas (nombre_completo) VALUES (%s) ON CONFLICT DO NOTHING;",
                                (nombre,)
                            )
                    conn.commit()
        except Exception as e:
            raise Exception(f"Error al cargar nombres iniciales: {str(e)}")
