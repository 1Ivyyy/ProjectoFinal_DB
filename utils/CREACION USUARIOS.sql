CREATE ROLE rol_secretaria NOLOGIN;

insert into persona (persona_id, tipo_documento, nombres, apellidos, fecha_nacimiento, sexo, direccion, telefono, email) VALUES
(4012, 'CC', 'Camilo Andrés', 'Ospina Ramírez', '1987-05-30', 'M', 'Av. Los Comuneros #55-20', '3157890123', 'camilo.ospina@esperanza.com')

insert into rol_persona (id_rol, persona_id) values
(7,4012)

select * from persona
select * from rol_persona
select * from rol

insert into rol (id_rol, nombre_rol) VALUES (7,'administrador');

delete from persona where persona_id = 4013

CREATE USER "4001" WITH PASSWORD 'usuario4001';
GRANT rol_doctor TO "4001";

CREATE USER "4002" WITH PASSWORD 'usuario4002';
GRANT rol_doctor TO "4002";

CREATE USER "4003" WITH PASSWORD 'usuario4003';
GRANT rol_doctor TO "4003";
GRANT rol_usuario TO "4003";

CREATE USER "4004" WITH PASSWORD 'usuario4004';
GRANT rol_tecnico TO "4004";

CREATE USER "4005" WITH PASSWORD 'usuario4005';
GRANT rol_tecnico TO "4005";

CREATE USER "4006" WITH PASSWORD 'usuario4006';
GRANT rol_usuario TO "4006";

CREATE USER "4007" WITH PASSWORD 'usuario4007';
GRANT rol_usuario TO "4007";

CREATE USER "4008" WITH PASSWORD 'usuario4008';
GRANT rol_usuario TO "4008";

CREATE USER "4009" WITH PASSWORD 'usuario4009';
GRANT rol_usuario TO "4009";

CREATE USER "4010" WITH PASSWORD 'usuario4010';
GRANT rol_usuario TO "4010";

CREATE USER "4011" WITH PASSWORD 'usuario4011';
GRANT rol_usuario TO "4011";

CREATE USER "4012" WITH PASSWORD 'usuario4012';
GRANT rol_admin_sistema TO "4012";

CREATE USER "4014" WITH PASSWORD 'usuario4014';
GRANT rol_secretaria TO "4014";

