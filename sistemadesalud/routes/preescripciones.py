from flask import Blueprint, jsonify
from db import get_connection
from session_manager import get_credentials
from flask import request
from session_manager import get_session
from session_manager import set_credentials

preescripciones_bp = Blueprint("preescripciones", __name__)

@preescripciones_bp.get("/paciente/listar")
def listar_preescripciones():
    
    session = get_session()
    persona_id = 4003
    try:
        set_credentials("4003", "alejandro123")
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()
    
    listar_preescripciones_query = """
    select m.nombre as medicamento, m.descripcion, pr.dosis, pr.frecuencia, pr.duracion, 
    pr.fecha_emision, vd.nombres as nombre_medico, vd.apellidos as apellido_medico
    from prescripciones pr 
    natural join paciente pa  
    natural join medicamentos m 
    natural join vista_doctores vd
    where pa.persona_id = %s
    order by pr.fecha_emision desc;
    """ 
    try:
        cur.execute(listar_preescripciones_query, (persona_id,))
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

@preescripciones_bp.post("/doctor/listar/paciente")
def listar_preescripciones_paciente():
    data = request.json
    persona_id = data.get("persona_id")
    
    try:
        set_credentials("4003", "alejandro123")
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()
    
    listar_preescripciones_query = """
    select m.nombre as medicamento, m.descripcion, pr.dosis, pr.frecuencia, pr.duracion, 
    pr.fecha_emision, vd.nombres as nombre_medico, vd.apellidos as apellido_medico
    from prescripciones pr 
    natural join paciente pa  
    natural join medicamentos m 
    natural join vista_doctores vd
    where pa.persona_id = %s
    order by pr.fecha_emision desc;
    """  
    try:
        cur.execute(listar_preescripciones_query, (persona_id,))
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200

@preescripciones_bp.post("/escribir")
def escribir():
    data = request.json
    persona_id = data.get("persona_id")
    
    try:
        set_credentials("4003", "alejandro123")
        conn = get_connection()
    except Exception as e:
        return jsonify({"error": str(e)}), 401   # No hay login o credenciales inválidas

    cur = conn.cursor()
    
    listar_preescripciones_query = """
    select m.nombre as medicamento, m.descripcion, pr.dosis, pr.frecuencia, pr.duracion, 
    pr.fecha_emision, vd.nombres as nombre_medico, vd.apellidos as apellido_medico
    from prescripciones pr 
    natural join paciente pa  
    natural join medicamentos m 
    natural join vista_doctores vd
    where pa.persona_id = %s
    order by pr.fecha_emision desc;
    """  
    try:
        cur.execute(listar_preescripciones_query, (persona_id,))
        rows = cur.fetchall()
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": f"Error ejecutando consulta: {str(e)}"}), 500

    cur.close()
    conn.close()

    return jsonify(rows), 200