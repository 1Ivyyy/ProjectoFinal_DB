from flask import Blueprint, request, jsonify
import psycopg2
from session_manager import (
    set_app_credentials, set_credentials, set_session,
    clear_session, get_session
)

auth_bp = Blueprint("auth", __name__)

DB_CONFIG = {
    "host": "localhost",
    "dbname": "sistemadesalud"
}


# ------------------------------
#  PASO 1: LOGIN POR PERSONA_ID
# ------------------------------
@auth_bp.post("/login")
def login():
    data = request.json
    persona_id = data.get("persona_id")
    password = data.get("password")

    if not persona_id or not password:
        return jsonify({"error": "persona_id y password son requeridos"}), 400

    # ---------------------------
    # 1. Conectamos con usuario 'app'
    # ---------------------------
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            dbname=DB_CONFIG["dbname"],
            user="app",
            password="app123"
        )
        set_app_credentials()
    except Exception:
        return jsonify({"error": "Error conectando con usuario APP"}), 500

    cur = conn.cursor()

    # 2. Obtener roles del usuario
    q = """
        SELECT r.nombre_rol
        FROM rol_persona rp
        NATURAL JOIN rol r
        WHERE rp.persona_id = %s;
    """
    cur.execute(q, (persona_id,))
    roles = [r[0] for r in cur.fetchall()]

    if not roles:
        return jsonify({"error": "La persona no tiene roles registrados"}), 401

    # Guardamos el persona_id
    cur.close()
    conn.close()

    # Usuario REAL = persona_id
    actual_user = str(persona_id)

    # ---------------------------
    #  Si solo tiene un rol → login directo
    # ---------------------------
    if len(roles) == 1:
        role = roles[0]

        # Intentar conexión real con credenciales del usuario
        try:
            real_conn = psycopg2.connect(
                host=DB_CONFIG["host"],
                dbname=DB_CONFIG["dbname"],
                user=actual_user,
                password=password
            )
            real_conn.close()
        except Exception:
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Guardar credenciales reales
        set_credentials(actual_user, password)

        # Guardar sesión con el rol único
        set_session(persona_id, roles, active_role=role)

        return jsonify({
            "message": "Login exitoso",
            "persona_id": persona_id,
            "roles": roles,
            "active_role": role
        }), 200

    # ---------------------------
    #  Si tiene múltiples roles → front debe pedir selección
    # ---------------------------
    return jsonify({
        "message": "Selecciona un rol",
        "persona_id": persona_id,
        "roles": roles,
        "requires_role_selection": True
    }), 200



# ------------------------------
#  PASO 2: CONFIRMAR ROL
# ------------------------------
@auth_bp.post("/login/confirm-role")
def confirm_role():
    data = request.json
    persona_id = data.get("persona_id")
    selected_role = data.get("role")
    password = data.get("password")

    if not persona_id or not selected_role or not password:
        return jsonify({"error": "persona_id, role y password son requeridos"}), 400

    actual_user = str(persona_id)

    # Validar credenciales reales
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            dbname=DB_CONFIG["dbname"],
            user=actual_user,
            password=password
        )
        conn.close()
    except Exception:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Guardar credenciales reales
    set_credentials(actual_user, password)

    # Actualizar el rol activo
    roles = [selected_role]
    set_session(persona_id, roles, active_role=selected_role)

    return jsonify({
        "message": "Rol activado exitosamente",
        "persona_id": persona_id,
        "active_role": selected_role
    }), 200
