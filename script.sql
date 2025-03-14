CREATE DATABASE IF NOT EXISTS healthgrid DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- Todos os deltas estão em segundos

USE healthgrid;

-- Cada uma das 8 zonas (0 ... 7) será mapeada como um id_sensor (1 ... 8)
-- topic espm/stainel/hpd/DetectedPersonsZone
-- {"DetectedPersonsZone":[0,0,2,1,1,0,1,0]}
-- topic espm/stainel/hpd/LuxZone
-- {"LuxZone":[70.00,78.00,74.00,87.00,67.00,57.00,50.00,53.00]}
-- topic espm/stainel/hpd/Humidity
-- {"Humidity":67.00}
-- topic espm/stainel/hpd/Temperature
-- {"Temperature":24.30}
CREATE TABLE pca (
  id bigint NOT NULL AUTO_INCREMENT,
  data datetime NOT NULL,
  id_sensor tinyint NOT NULL,
  id_especialidade tinyint NOT NULL,
  delta int NOT NULL, -- O campo delta diz respeito a alterações no valor de pessoas
  pessoas tinyint NOT NULL,
  luminosidade float NOT NULL,
  umidade float NOT NULL,
  temperatura float NOT NULL,
  PRIMARY KEY (id),
  KEY pca_data_id_sensor (data, id_sensor),
  KEY pca_id_sensor (id_sensor)
);

-- Query para monitorar em tempo real
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 1 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 2 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 3 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 4 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 5 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 6 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 7 order by id desc limit 1)
union all
(select id_sensor, id_especialidade, case pessoas when 0 then 0 else 1 end ocupacao, data from pca where id_sensor = 8 order by id desc limit 1)
;

-- Query com a ocupação booleana por dia
select id_sensor, id_especialidade, case max(pessoas) when 0 then 0 else 1 end ocupacao, date(data) dia from pca
where data between '2025-03-10 00:00:00' and '2025-03-14 23:59:59'
group by id_sensor, id_especialidade, dia
order by id_sensor, id_especialidade, dia
;
