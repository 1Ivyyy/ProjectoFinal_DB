from flask import Blueprint, request, jsonify
from db import get_connection
from session_manager import set_credentials

register_bp = Blueprint("register", __name__)

## Registro de Paciente
@register_bp.post("/paciente")
def registrar_paciente():
    data = request.json

    try:
        set_credentials("app", "app123")
        conn = get_connection()
        cur = conn.cursor()

        # -----------------------------
        # 1. INSERT en PERSONA
        # -----------------------------
        insert_persona_query = """
            INSERT INTO persona 
            (persona_id, tipo_documento, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, email)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING persona_id;
        """

        persona_values = (
            data["persona_id"],
            data["tipo_documento"],
            data["nombres"],
            data["apellidos"],
            data["fecha_nacimiento"],
            data["sexo"],
            data["direccion"],
            data["telefono"],
            data["email"]
        )

        cur.execute(insert_persona_query, persona_values)
        persona_id = cur.fetchone()[0]

        # -----------------------------
        # 2. INSERT en PACIENTE
        # -----------------------------
        insert_paciente_query = """
            INSERT INTO paciente 
            (persona_id, tipo_sangre, contacto_emergencia, riesgo_clinico)
            VALUES (%s, %s, %s, %s)
            RETURNING paciente_id;
        """

        paciente_values = (
            persona_id,
            data["tipo_sangre"],
            data["contacto_emergencia"],
            data["riesgo_clinico"]
        )

        cur.execute(insert_paciente_query, paciente_values)
        paciente_id = cur.fetchone()[0]

        # 3. CREAR USUARIO EN POSTGRES
        username = str(data["persona_id"])
        password = data["password"]

        crear_usuario_query = f'CREATE USER "{username}" WITH PASSWORD %s;'
        cur.execute(crear_usuario_query, (password,))

        # 4. ASIGNAR ROL
        asignar_rol_query = f'GRANT rol_usuario TO "{username}";'
        cur.execute(asignar_rol_query)
        
        # 5. Agregarlo a Rol_Persona siendo Paciente
        agregar_rol_persona_query = f'INSERT INTO rol_persona (id_rol, persona_id) VALUES (2,{persona_id})'
        cur.execute(agregar_rol_persona_query)
        
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Paciente registrado exitosamente",
            "persona_id": persona_id,
            "paciente_id": paciente_id,
            "usuario_creado": username
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
## Registro de Doctor
@register_bp.post("/doctor")
def registrar_doctor():
    data = request.json

    try:
        set_credentials("app", "app123")
        conn = get_connection()
        cur = conn.cursor()

        # -----------------------------
        # 1. INSERT en PERSONA
        # -----------------------------
        insert_persona_query = """
            INSERT INTO persona 
            (persona_id, tipo_documento, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, email)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING persona_id;
        """

        persona_values = (
            data["persona_id"],
            data["tipo_documento"],
            data["nombres"],
            data["apellidos"],
            data["fecha_nacimiento"],
            data["sexo"],
            data["direccion"],
            data["telefono"],
            data["email"]
        )

        cur.execute(insert_persona_query, persona_values)
        persona_id = cur.fetchone()[0]
        
        # -----------------------------
        # 2. INSERT en EMPLEADO
        # -----------------------------
        insert_empleado_query = """
            INSERT INTO empleado 
            (persona_id, departamento_id, sede_id, fecha_contratacion, salario)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING empleado_id;
        """

        empleado_values = (
            persona_id,
            data["departamento_id"],
            data["sede_id"],
            data["fecha_contratacion"],
            data["salario"]
        )

        cur.execute(insert_empleado_query, empleado_values)
        empleado_id = cur.fetchone()[0]

        # -----------------------------
        # 3. INSERT en Doctor
        # -----------------------------
        insert_doctor_query = """
            INSERT INTO doctor 
            (empleado_id, especialidad)
            VALUES (%s, %s)
            RETURNING doctor_id;
        """

        doctor_values = (
            empleado_id,
            data["especialidad"]
        )

        cur.execute(insert_doctor_query, doctor_values)
        doctor_id = cur.fetchone()[0]

        # 3. CREAR USUARIO EN POSTGRES
        username = str(doctor_id)
        password = data["password"]

        crear_usuario_query = f'CREATE USER "{username}" WITH PASSWORD %s;'
        cur.execute(crear_usuario_query, (password,))

        # 4. ASIGNAR ROL
        asignar_rol_query = f'GRANT rol_doctor TO "{username}";'
        cur.execute(asignar_rol_query)
        
        # 5. Agregarlo a Rol_Persona siendo Doctor
        agregar_rol_persona_query = f'INSERT INTO rol_persona (id_rol, persona_id) VALUES (1,{persona_id})'
        cur.execute(agregar_rol_persona_query)
        
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Doctor registrado exitosamente",
            "persona_id": persona_id,
            "doctor_id": doctor_id,
            "usuario_creado": username
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    ## Registro de Tecnico
@register_bp.post("/tecnico")
def registrar_tecnico():
    data = request.json

    try:
        set_credentials("app", "app123")
        conn = get_connection()
        cur = conn.cursor()

        # -----------------------------
        # 1. INSERT en PERSONA
        # -----------------------------
        insert_persona_query = """
            INSERT INTO persona 
            (persona_id, tipo_documento, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, email)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING persona_id;
        """

        persona_values = (
            data["persona_id"],
            data["tipo_documento"],
            data["nombres"],
            data["apellidos"],
            data["fecha_nacimiento"],
            data["sexo"],
            data["direccion"],
            data["telefono"],
            data["email"]
        )

        cur.execute(insert_persona_query, persona_values)
        persona_id = cur.fetchone()[0]
        
        # -----------------------------
        # 2. INSERT en EMPLEADO
        # -----------------------------
        insert_empleado_query = """
            INSERT INTO empleado 
            (persona_id, departamento_id, sede_id, fecha_contratacion, salario)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING empleado_id;
        """

        empleado_values = (
            persona_id,
            data["departamento_id"],
            data["sede_id"],
            data["fecha_contratacion"],
            data["salario"]
        )

        cur.execute(insert_empleado_query, empleado_values)
        empleado_id = cur.fetchone()[0]

        # -----------------------------
        # 3. INSERT en Tecnico
        # -----------------------------
        insert_tecnico_query = """
            INSERT INTO tecnico 
            (empleado_id, area) 
            VALUES (%s, %s)
            RETURNING tecnico_id;
        """

        tecnico_values = (
            empleado_id,
            data["area"]
        )

        cur.execute(insert_tecnico_query, tecnico_values)
        tecnico_id = cur.fetchone()[0]

        # 3. CREAR USUARIO EN POSTGRES
        username = str(tecnico_id)
        password = data["password"]

        crear_usuario_query = f'CREATE USER "{username}" WITH PASSWORD %s;'
        cur.execute(crear_usuario_query, (password,))

        # 4. ASIGNAR ROL
        asignar_rol_query = f'GRANT rol_tecnico TO "{username}";'
        cur.execute(asignar_rol_query)
        
        # 5. Agregarlo a Rol_Persona siendo Doctor
        agregar_rol_persona_query = f'INSERT INTO rol_persona (id_rol, persona_id) VALUES (5,{persona_id})'
        cur.execute(agregar_rol_persona_query)
        
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Tecnico registrado exitosamente",
            "persona_id": persona_id,
            "tecnico_id": tecnico_id,
            "usuario_creado": username
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
