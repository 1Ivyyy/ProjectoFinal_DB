from flask import Blueprint, jsonify
from db import get_connection

pacientes_bp = Blueprint("pacientes", __name__)

@pacientes_bp.get("/")
def listar_pacientes():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM paciente;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

