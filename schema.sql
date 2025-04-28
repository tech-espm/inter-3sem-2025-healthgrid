-- Criação das tabelas para o sistema HealthGrid

-- Tabela de setores do hospital
CREATE TABLE IF NOT EXISTS setores_hospital (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setor VARCHAR(100) NOT NULL,
    capacidade_maxima INT NOT NULL,
    descricao TEXT
);

-- Tabela de pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(200) NOT NULL,
    data_nascimento DATE,
    status ENUM('internado', 'alta', 'transferido') NOT NULL DEFAULT 'internado'
);

-- Tabela de atendimentos
CREATE TABLE IF NOT EXISTS atendimentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT,
    data_entrada DATETIME NOT NULL,
    data_saida DATETIME,
    tipo_atendimento VARCHAR(100),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- Tabela de ocupação de leitos
CREATE TABLE IF NOT EXISTS ocupacao_leitos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setor_id INT,
    paciente_id INT,
    data_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (setor_id) REFERENCES setores_hospital(id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- Inserir alguns dados de exemplo nos setores
INSERT INTO setores_hospital (setor, capacidade_maxima, descricao) VALUES
('UTI', 20, 'Unidade de Terapia Intensiva'),
('Emergência', 30, 'Pronto Socorro'),
('Pediatria', 25, 'Ala Infantil'),
('Cardiologia', 15, 'Centro Cardíaco'),
('Ortopedia', 20, 'Centro Ortopédico');

-- Inserir alguns pacientes de exemplo
INSERT INTO pacientes (nome, data_nascimento, status) VALUES
('João Silva', '1980-05-15', 'internado'),
('Maria Santos', '1992-08-22', 'internado'),
('Pedro Oliveira', '1975-03-10', 'internado'),
('Ana Costa', '1988-12-03', 'internado');

-- Inserir alguns atendimentos
INSERT INTO atendimentos (paciente_id, data_entrada, data_saida, tipo_atendimento) VALUES
(1, CURRENT_DATE, NULL, 'Emergência'),
(2, CURRENT_DATE, DATE_ADD(CURRENT_DATE, INTERVAL 2 HOUR), 'Consulta'),
(3, CURRENT_DATE, NULL, 'Internação'),
(4, CURRENT_DATE, NULL, 'Emergência');

-- Inserir ocupações de leitos
INSERT INTO ocupacao_leitos (setor_id, paciente_id, data_registro) VALUES
(1, 1, CURRENT_TIMESTAMP),
(2, 2, CURRENT_TIMESTAMP),
(3, 3, CURRENT_TIMESTAMP),
(4, 4, CURRENT_TIMESTAMP);
