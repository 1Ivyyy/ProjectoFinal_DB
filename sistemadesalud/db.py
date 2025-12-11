
from config import POSTGRES_CONFIG
from session_manager import get_credentials
import psycopg2

def get_connection():
    user, password = get_credentials()

    if not user or not password:
        raise Exception("No hay credenciales activas. Debes iniciar sesión.")

    return psycopg2.connect(
        host=POSTGRES_CONFIG['host'],
        dbname=POSTGRES_CONFIG['dbname'],
        port=POSTGRES_CONFIG['port'],
        user=user,
        password=password
    )


    
