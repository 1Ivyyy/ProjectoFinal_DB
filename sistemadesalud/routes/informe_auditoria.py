from flask import Blueprint, jsonify
from db import get_connection
from session_manager import set_credentials

informe_bp = Blueprint("informe", __name__)

@informe_bp.get("/generar")
def generar_informe():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_auditorias_ultimos_10_accesos_global;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200



    


