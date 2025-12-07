
# Manejo simple de sesión en memoria (suficiente para un proyecto académico)
session_data = {
    "user": None,
    "password": None
}

def set_credentials(user, password):
    session_data["user"] = user
    session_data["password"] = password

def get_credentials():
    return session_data["user"], session_data["password"]