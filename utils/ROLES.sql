
-- ROLES FUNCIONALES
CREATE ROLE rol_doctor NOLOGIN;
CREATE ROLE rol_tecnico NOLOGIN;
CREATE ROLE rol_usuario NOLOGIN; 
CREATE ROLE rol_secretaria NOLOGIN;
CREATE ROLE rol_admin_sistema NOLOGIN;

-- ROL DOCTOR

GRANT SELECT, INSERT ON historias_clinicas TO rol_doctor;
GRANT SELECT, INSERT ON prescripciones TO rol_doctor;
GRANT SELECT ON citas TO rol_doctor;
GRANT SELECT ON paciente TO rol_doctor;
GRANT SELECT ON persona TO rol_doctor;

-- ROL SECRETARIA 

GRANT SELECT, INSERT ON, UPDATE, DELETE citas TO rol_secretaria;


-- ROL TECNICO

GRANT SELECT, UPDATE ON equipamiento TO rol_tecnico;
GRANT SELECT, INSERT ON mantenimiento TO rol_tecnico;

-- ROL USUARIO

GRANT SELECT, INSERT, UPDATE ON citas TO rol_usuario;
GRANT SELECT ON paciente TO rol_usuario;
GRANT SELECT ON persona TO rol_usuario;

-- ROL APP

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app;


-- REVOCAR ACCESOS PÚBLICOS (recomendado)

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- PERMISOS ROL ADMINISTRADOR EN VISTAS

-- CONSULTA 1
GRANT SELECT ON vista_medicamentos_recetados_mes_global TO rol_admin_sistema 
GRANT SELECT ON vista_medicamentos_recetados_mes_azure TO rol_admin_sistema
GRANT SELECT ON vista_medicamentos_recetados_mes_aws TO rol_admin_sistema
GRANT SELECT ON vista_medicamentos_recetados_mes_local TO rol_admin_sistema
-- CONSULTA 2
GRANT SELECT ON vista_medicos_mas_consultas_semana_global TO rol_admin_sistema
GRANT SELECT ON vista_medicos_mas_consultas_semana_local TO rol_admin_sistema
GRANT SELECT ON vista_medicos_mas_consultas_semana_azure TO rol_admin_sistema
GRANT SELECT ON vista_medicos_mas_consultas_semana_aws TO rol_admin_sistema
-- CONSULTA 3
GRANT SELECT ON vista_tiempo_prom_cita_y_diagnostico_pereira TO rol_admin_sistema
GRANT SELECT ON vista_tiempo_prom_cita_y_diagnostico_cali TO rol_admin_sistema
GRANT SELECT ON vista_tiempo_prom_cita_y_diagnostico_bogota TO rol_admin_sistema
GRANT SELECT ON vista_tiempo_prom_cita_y_diagnostico_global TO rol_admin_sistema
-- CONSULTA 4
GRANT SELECT ON vista_auditorias_ultimos_10_accesos_local TO rol_admin_sistema
GRANT SELECT ON vista_auditorias_ultimos_10_accesos_cali TO rol_admin_sistema
GRANT SELECT ON vista_auditorias_ultimos_10_accesos_bogota TO rol_admin_sistema
GRANT SELECT ON vista_auditorias_ultimos_10_accesos_global TO rol_admin_sistema
-- CONSULTA 5
GRANT SELECT ON vista_departamentos_comparten_equipamiento_otra_sede_local TO rol_admin_sistema
GRANT SELECT ON vista_departamentos_comparten_equipamiento_otra_sede_aws TO rol_admin_sistema
GRANT SELECT ON vista_departamentos_comparten_equipamiento_otra_sede_azure TO rol_admin_sistema
GRANT SELECT ON vista_departamentos_comparten_equipamiento_otra_sede_global TO rol_admin_sistema
-- CONSULTA 6
GRANT SELECT ON vista_pacientes_atendidos_enfermedad_sede_local TO rol_admin_sistema
GRANT SELECT ON vista_pacientes_atendidos_enfermedad_sede_aws TO rol_admin_sistema
GRANT SELECT ON vista_pacientes_atendidos_enfermedad_sede_azure TO rol_admin_sistema
GRANT SELECT ON vista_pacientes_atendidos_enfermedad_sede_global TO rol_admin_sistema

