from flask import Blueprint, jsonify
from db import get_connection
from session_manager import set_credentials

doctores_bp = Blueprint("doctores", __name__)

## Doctores mas consultados por Sede (Pereira)
@doctores_bp.get("/top_pereira")
def top_doctores_pereira():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("select * from vista_medicos_mas_consultas_semana_local;")
        rows = cur.fetchall() 
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

## Doctores mas consultados por Sede (Bogota)
@doctores_bp.get("/top_bogota")
def top_doctores_bogota():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("select * from vista_medicos_mas_consultas_semana_azure;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

## Doctores mas consultados por Sede (Cali)
@doctores_bp.get("/top_cali")
def top_doctores_cali():
    try:
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM vista_medicos_mas_consultas_semana_aws;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

## Medicamentos mas recetados GLOBAL
@doctores_bp.get("/top_global")
def top_doctores_global():
    try:
        set_credentials ('postgres','root12345')
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()

    try:
        cur.execute("select * from vista_medicos_mas_consultas_semana_global;")
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200


    


