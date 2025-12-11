
-- consulta 1 medicamentos mas recetados en el mes 
select * from vista_medicamentos_recetados_mes_azure

create view vista_medicamentos_recetados_mes_azure as
SELECT s."sede_id",
       s."nombre" AS sede,
       t.medicamento,
       t.total_recetas
FROM "sede" s
JOIN LATERAL (
  SELECT m."nombre" AS medicamento,
         COUNT(*)   AS total_recetas
  FROM "prescripciones" p
  JOIN "medicamentos"   m ON m."medicamento_id" = p."medicamento_id"
  WHERE p."sede_id" = s."sede_id"
    AND p."fecha_emision" >= (CURRENT_DATE - INTERVAL '30 days')
  GROUP BY m."nombre"
  ORDER BY COUNT(*) DESC, m."nombre"
  LIMIT 5
) AS t ON TRUE
ORDER BY s."sede_id", t.total_recetas DESC, t.medicamento;
--consulta 2 medicos con mayor numero de consultas en la semana 

select * from vista_medicos_mas_consultas_semana_azure
create view vista_medicos_mas_consultas_semana_azure as
SELECT 
    semana,
    medico,
    sede_nombre,
    ciudad,
    consultas_atendidas,
    ranking
FROM (
    SELECT 
        TO_CHAR(c.fecha_hora, 'YYYY-"W"IW') AS semana,
        CONCAT(p.nombres, ' ', p.apellidos) AS medico,
        s.nombre AS sede_nombre,
        -- Extraer ciudad con manejo de casos sin coma
        CASE 
            WHEN s.direccion LIKE '%,%' THEN TRIM(SPLIT_PART(s.direccion, ',', -1))
            ELSE 'Ciudad no especificada'
        END AS ciudad,
        COUNT(*) AS consultas_atendidas,
        ROW_NUMBER() OVER (
            PARTITION BY TO_CHAR(c.fecha_hora, 'YYYY-"W"IW') 
            ORDER BY COUNT(*) DESC
        ) AS ranking
    FROM citas c
    JOIN doctor d ON c.doctor_id = d.doctor_id
    JOIN empleado e ON d.empleado_id = e.empleado_id
    JOIN persona p ON e.persona_id = p.persona_id
    JOIN sede s ON c.sede_id = s.sede_id
    WHERE c.estado = 'Completada'
        AND c.fecha_hora >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 
        TO_CHAR(c.fecha_hora, 'YYYY-"W"IW'), 
        CONCAT(p.nombres, ' ', p.apellidos), 
        s.nombre,
        CASE 
            WHEN s.direccion LIKE '%,%' THEN TRIM(SPLIT_PART(s.direccion, ',', -1))
            ELSE 'Ciudad no especificada'
        END
) ranked
WHERE ranking <= 3
ORDER BY semana DESC, ranking ASC;

-----tiempo promedio cita y registro de diagnostico
select * from vista_medicos_mas_consultas_semana_azure
create view vista_tiempo_prom_cita_y_diagnostico_azure as
SELECT
  c.sede_id,
  s.nombre AS sede,
  CONCAT(
    FLOOR(EXTRACT(EPOCH FROM AVG(h.fecha_registro - c.fecha_hora)) / 3600), 'h ',
    LPAD(FLOOR(MOD(EXTRACT(EPOCH FROM AVG(h.fecha_registro - c.fecha_hora)), 3600) / 60)::TEXT, 2, '0'), 'm'
  ) AS tiempo_promedio_espera
FROM prescripciones p
JOIN historias_clinicas h ON h.historia_id = p.historia_id
JOIN citas c ON c.cita_id = p.cita_id
JOIN sede s ON s.sede_id = c.sede_id
WHERE c.estado = 'Completada'
GROUP BY c.sede_id, s.nombre
ORDER BY c.sede_id;

----consulta 4 Generar un informe de auditoría con los últimos 10 accesos a la tabla Historias_Clinicas muestra nombre usuario y rol
select * from vista_auditorias_ultimos_10_accesos_azure
create view vista_auditorias_ultimos_10_accesos_azure as
SELECT
  a.fecha_evento,
  a.accion,
  a.ip_origen,
  per.nombres || ' ' || per.apellidos AS usuario,
  COALESCE(string_agg(DISTINCT r.nombre_rol, ', ' ORDER BY r.nombre_rol), 'Sin rol asignado') AS roles,
  CASE 
    WHEN sede.direccion LIKE '%,%' THEN 
      TRIM(SPLIT_PART(sede.direccion, ',', -1))
    ELSE 
      sede.direccion 
  END AS ciudad,
  sede.nombre AS sede
FROM auditoria_accesos a
JOIN persona per ON per.persona_id = a.persona_id
LEFT JOIN rol_persona rp ON rp.persona_id = per.persona_id
LEFT JOIN rol r ON r.id_rol = rp.id_rol
-- Unir con empleado para obtener la sede
LEFT JOIN empleado emp ON emp.persona_id = per.persona_id
-- Unir con sede para obtener la dirección (que contiene la ciudad) y nombre de sede
LEFT JOIN sede ON sede.sede_id = emp.sede_id
WHERE LOWER(a.tabla_modificada) = 'historias_clinicas'
GROUP BY
  a.evento_id, a.fecha_evento, a.accion, a.ip_origen,
  per.persona_id, per.nombres, per.apellidos, sede.direccion, sede.nombre
ORDER BY a.fecha_evento DESC
LIMIT 10;

--consulta 5 los depatamentos que comparten equipamiento con otra sede
select * from comparte
select * from vista_departamentos_comparten_equipamiento_otra_sede_azure
create view vista_departamentos_comparten_equipamiento_otra_sede_azure as
SELECT
  e."equipamiento_id",
  e."nombre" AS equipo,
  e."categoria",
  MIN(d."nombre") AS departamento,
  COUNT(DISTINCT c."sede_id") AS num_sedes,
  -- Lista de sedes donde está el equipo
  STRING_AGG(DISTINCT s."nombre", ', ' ORDER BY s."nombre") AS sedes,
  -- Lista de ciudades donde está el equipo (extraídas de la dirección)
  STRING_AGG(
    DISTINCT 
    CASE 
      WHEN s."direccion" LIKE '%,%' THEN 
        TRIM(SPLIT_PART(s."direccion", ',', -1))
      ELSE 
        s."direccion"
    END, 
    ', ' 
    ORDER BY 
    CASE 
      WHEN s."direccion" LIKE '%,%' THEN 
        TRIM(SPLIT_PART(s."direccion", ',', -1))
      ELSE 
        s."direccion"
    END
  ) AS ciudades
FROM "comparte" c
JOIN "equipamiento" e ON e."equipamiento_id" = c."equipamiento_id"
JOIN "departamento" d ON d."departamento_id" = c."departamento_id" 
  AND d."sede_id" = c."sede_id"
JOIN "sede" s ON s."sede_id" = c."sede_id"
GROUP BY e."equipamiento_id", e."nombre", e."categoria", c."departamento_id"
HAVING COUNT(DISTINCT c."sede_id") > 1
ORDER BY equipo, c."departamento_id";

--6 total de pacientes atendidos por enfermedad y por sede
select * from vista_pacientes_atendidos_enfermedad_sede_azure
create view vista_pacientes_atendidos_enfermedad_sede_azure as
SELECT
  c."sede_id",
  s."nombre" AS sede,
  -- Extraer la ciudad de la dirección de la sede
  CASE 
    WHEN s."direccion" LIKE '%,%' THEN 
      TRIM(SPLIT_PART(s."direccion", ',', -1))
    ELSE 
      s."direccion"
  END AS ciudad,
  h."diagnostico",
  COUNT(DISTINCT h."paciente_id") AS pacientes_unicos
FROM "prescripciones" p
JOIN "citas"             c ON c."cita_id"     = p."cita_id"
JOIN "historias_clinicas" h ON h."historia_id" = p."historia_id"
JOIN "sede"              s ON s."sede_id"     = c."sede_id"
WHERE c."estado" = 'Completada'
  AND NOT EXISTS (
      SELECT 1
      FROM "prescripciones" q
      WHERE q."cita_id" = p."cita_id"
        AND q."historia_id" = p."historia_id"
        AND q."prescripcion_id" < p."prescripcion_id"
  )
GROUP BY c."sede_id", s."nombre", s."direccion", h."diagnostico"
ORDER BY c."sede_id", pacientes_unicos DESC, h."diagnostico";


