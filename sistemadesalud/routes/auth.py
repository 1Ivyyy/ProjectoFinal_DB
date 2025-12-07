
from flask import Blueprint, request, jsonify
import psycopg2
from session_manager import set_credentials

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.json
    user = data.get("user")
    password = data.get("password")

    # Intentar conexión para validar credenciales
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="tu_base",
            user=user,
            password=password
        )
        conn.close()
        set_credentials(user, password)
        return jsonify({"message": "Login exitoso"}), 200

    except Exception as e:
        return jsonify({"error": "Credenciales inválidas"}), 401
