import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Settings:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "blacklist_db")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "postgres123")
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta_super_segura_aqui_cambiar_en_produccion")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.valid_test_token = os.getenv(
            "VALID_TEST_TOKEN",
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjk5OTk5OTk5OTl9.Jz8n5r7Y5oU8i6A2cX4l8N3vB9u1K6t3R7yW5qE8zF2"
        )

    @property
    def database_url(self):
        return f"dbname={self.db_name} user={self.db_user} password={self.db_password} host={self.db_host} port={self.db_port}"

def get_connection():
    """Devuelve una conexión nueva a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise Exception(f"Error de conexión a la base de datos: {str(e)}")

settings = Settings()
