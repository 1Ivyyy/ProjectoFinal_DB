from flask import Blueprint, jsonify
from db import get_connection
from session_manager import set_credentials

pacientes_bp = Blueprint("pacientes", __name__)

@pacientes_bp.get("/pereira")
def listar_pacientes_pereira():
    try:
        set_credentials("postgres", "root12345")
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_pacientes_atendidos_enfermedad_sede_local limit 6;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

@pacientes_bp.get("/bogota")
def listar_pacientes_bogota():
    try:
        set_credentials("postgres", "root12345")
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_pacientes_atendidos_enfermedad_sede_azure limit 6;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

@pacientes_bp.get("/cali")
def listar_pacientes_cali():
    try:
        set_credentials("postgres", "root12345")
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_pacientes_atendidos_enfermedad_sede_aws limit 6;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

@pacientes_bp.get("/global")
def listar_pacientes_global():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_pacientes_atendidos_enfermedad_sede_global limit 6;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200