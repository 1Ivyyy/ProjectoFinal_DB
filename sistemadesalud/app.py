
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.register import register_bp
from routes.pacientes import pacientes_bp
from routes.cita import cita_bp
from routes.medicamentos import medicamentos_bp
from routes.doctores import doctores_bp
from routes.preescripciones import preescripciones_bp
from routes.promedio_tiempo_cita import promedio_bp
from routes.informe_auditoria import informe_bp
from routes.equipamiento_compartido import equipamiento_bp

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(register_bp, url_prefix="/register")
app.register_blueprint(pacientes_bp, url_prefix="/pacientes")
app.register_blueprint(cita_bp, url_prefix="/cita")
app.register_blueprint(medicamentos_bp, url_prefix="/medicamentos")
app.register_blueprint(doctores_bp, url_prefix="/doctores")
app.register_blueprint(preescripciones_bp, url_prefix="/preescripciones")  
app.register_blueprint(promedio_bp, url_prefix="/promedio") 
app.register_blueprint(informe_bp, url_prefix="/informe")
app.register_blueprint(equipamiento_bp, url_prefix="/equipamiento")

if __name__ == "__main__":
    app.run(debug=True)
