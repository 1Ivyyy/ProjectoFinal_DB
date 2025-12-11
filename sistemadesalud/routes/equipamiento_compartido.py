from flask import Blueprint, jsonify
from db import get_connection
from session_manager import set_credentials

equipamiento_bp = Blueprint("equipamiento", __name__)

## Equipamiento compartido
@equipamiento_bp.get("/")
def equipamiento_compartido():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_promedio_tiempo_cita;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200




    


