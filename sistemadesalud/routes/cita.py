from flask import Blueprint, request, jsonify
from db import get_connection
from session_manager import get_session, is_logged_in

cita_bp = Blueprint("citas", __name__)


# 1. AGENDAR CITA (solo paciente)
@cita_bp.post("/agendar")
def agendar():
    if not is_logged_in():
        return jsonify({"error": "Debe iniciar sesión"}), 403

   

    data = request.json
    requerido = ["paciente_id","departamento_id", "sede_id", "doctor_id", "fecha_hora", "tipo_servicio"]

    if not all(campo in data for campo in requerido):
        return jsonify({"error": "Faltan campos en el cuerpo de la solicitud"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO citas
            (paciente_id, departamento_id, sede_id, doctor_id, fecha_hora, estado, tipo_servicio)
            VALUES (%s, %s, %s, %s, %s, 'Programada', %s)
            RETURNING cita_id;
        """, (
            data["paciente_id"],
            data["departamento_id"],
            data["sede_id"],
            data["doctor_id"],
            data["fecha_hora"],
            data["tipo_servicio"]
        ))

        cita_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({
            "message": "Cita agendada exitosamente",
            "cita_id": cita_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()



# 2. LISTAR CITAS (paciente o doctor)
@cita_bp.get("/listar")
def listar_citas():
    if not is_logged_in():
        return jsonify({"error": "Debe iniciar sesión"}), 403

    session = get_session()
    tipo = session["tipo"]

    try:
        conn = get_connection()
        cur = conn.cursor()


        # PACIENTE -> Listar sus citas
        if tipo == "paciente":
            paciente_id = session["paciente_id"]

            cur.execute("""
                SELECT cita_id, departamento_id, sede_id, doctor_id, fecha_hora, estado, tipo_servicio
                FROM citas
                WHERE paciente_id = %s
                ORDER BY fecha_hora;
            """, (paciente_id,))

        # DOCTOR -> Listar citas asignadas
        elif tipo == "doctor":
            doctor_id = session["doctor_id"]

            cur.execute("""
                SELECT cita_id, paciente_id, departamento_id, sede_id, fecha_hora, estado, tipo_servicio
                FROM citas
                WHERE doctor_id = %s
                ORDER BY fecha_hora;
            """, (doctor_id,))

        # TÉCNICO -> No tiene permisos
        else:
            return jsonify({"error": "Los técnicos no pueden ver citas"}), 403

        rows = cur.fetchall()

        # Convertir a JSON
        columnas = [desc[0] for desc in cur.description]
        citas = [dict(zip(columnas, fila)) for fila in rows]

        return jsonify({
            "tipo_usuario": tipo,
            "citas": citas
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


 
# 3. CANCELAR CITA (solo paciente)
@cita_bp.post("/cancelar")
def cancelar_cita():
    if not is_logged_in():
        return jsonify({"error": "Debe iniciar sesión"}), 403

    session = get_session()

    if session["tipo"] != "paciente":
        return jsonify({"error": "Solo un paciente puede cancelar citas"}), 403

    paciente_id = session["paciente_id"]
    data = request.json
    cita_id = data.get("cita_id")

    if not cita_id:
        return jsonify({"error": "Debe proporcionar cita_id"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Verificar que la cita le pertenece al paciente
        cur.execute("""
            SELECT * FROM citas
            WHERE cita_id = %s AND paciente_id = %s AND estado = 'Programada';
        """, (cita_id, paciente_id))

        if cur.fetchone() is None:
            return jsonify({"error": "No puede cancelar una cita que no le pertenece o que no está programada"}), 403

        # Cancelar
        cur.execute("DELETE FROM citas WHERE cita_id = %s;", (cita_id,))
        conn.commit()

        return jsonify({"message": "Cita cancelada exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

