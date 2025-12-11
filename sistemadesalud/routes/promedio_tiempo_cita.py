from flask import Blueprint, jsonify
from db import get_connection
from session_manager import set_credentials

promedio_bp = Blueprint("promedio", __name__)

## Medicamentos mas recetados por Sede (Pereira)
@promedio_bp.get("/pereira")
def promedio_tiempo_cita_pereira():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_tiempo_prom_cita_y_diagnostico_pereira;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

## Medicamentos mas recetados por Sede (Bogota)
@promedio_bp.get("/bogota")
def promedio_tiempo_cita_bogota():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_tiempo_prom_cita_y_diagnostico_bogota;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

## Medicamentos mas recetados por Sede (Cali)
@promedio_bp.get("/cali")
def promedio_tiempo_cita_cali():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_tiempo_prom_cita_y_diagnostico_cali;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

## Medicamentos mas recetados GLOBAL
@promedio_bp.get("/global")
def promedio_tiempo_cita_global():
    try:
        set_credentials ('postgres','root12345')
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("select * from vista_tiempo_prom_cita_y_diagnostico_global;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200


    


