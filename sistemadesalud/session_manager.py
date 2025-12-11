
SESSION_DATA = {
    "user": None,          # ← credenciales definitivas tras login exitoso
    "password": None,
    "persona_id": None,
    "roles": [],           # roles encontrados en la BD
    "active_role": None,   # ← el rol que eligió para entrar (solo 1)
}

def set_app_credentials():
    """Guarda las credenciales del usuario 'app' usadas SOLO para consultar roles."""
    SESSION_DATA["user"] = "app"
    SESSION_DATA["password"] = "app123"

def set_credentials(user, password):
    """Guarda credenciales del usuario REAL con el que se conectará PostgreSQL."""
    SESSION_DATA["user"] = user
    SESSION_DATA["password"] = password

def get_credentials():
    return SESSION_DATA["user"], SESSION_DATA["password"]

def set_session(persona_id, roles, active_role):
    SESSION_DATA["persona_id"] = persona_id
    SESSION_DATA["roles"] = roles
    SESSION_DATA["active_role"] = active_role

def get_session():
    return SESSION_DATA

def clear_session():
    for k in SESSION_DATA.keys():
        SESSION_DATA[k] = None

def is_logged_in():
    return SESSION_DATA["user"] is not None and SESSION_DATA["active_role"] is not None
