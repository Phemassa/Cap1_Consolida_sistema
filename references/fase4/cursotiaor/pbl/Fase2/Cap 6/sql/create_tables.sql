-- ============================================
-- FarmTech Solutions - Oracle Database Schema
-- Script de Criação de Tabelas
-- ============================================

-- Desabilita verificação de constraints (temporário)
SET CONSTRAINTS ALL DEFERRED;

-- =============================================
-- TABELA: CULTIVOS
-- Armazena dados dos cultivos cadastrados
-- =============================================
CREATE TABLE cultivos (
    id NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    cultura_tipo VARCHAR2(50) NOT NULL,
    area_hectares NUMBER(10,2) NOT NULL CHECK (area_hectares > 0),
    data_plantio DATE NOT NULL,
    nitrogenio_req NUMBER(5,2) CHECK (nitrogenio_req >= 0),
    fosforo_req NUMBER(5,2) CHECK (fosforo_req >= 0),
    potassio_req NUMBER(5,2) CHECK (potassio_req >= 0),
    ph_ideal NUMBER(3,1) CHECK (ph_ideal BETWEEN 3.0 AND 9.0),
    umidade_ideal NUMBER(5,2) CHECK (umidade_ideal BETWEEN 0 AND 100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para otimização de consultas
CREATE INDEX idx_cultivo_tipo ON cultivos(cultura_tipo);
CREATE INDEX idx_cultivo_plantio ON cultivos(data_plantio);

-- =============================================
-- TABELA: SENSORES
-- Armazena leituras dos sensores IoT
-- =============================================
CREATE TABLE sensores (
    id NUMBER(10) PRIMARY KEY,
    cultivo_id NUMBER(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperatura NUMBER(5,2) CHECK (temperatura BETWEEN -10 AND 50),
    umidade_ar NUMBER(5,2) CHECK (umidade_ar BETWEEN 0 AND 100),
    umidade_solo NUMBER(5,2) CHECK (umidade_solo BETWEEN 0 AND 100),
    ph NUMBER(3,1) CHECK (ph BETWEEN 3.0 AND 9.0),
    npk_n NUMBER(1) CHECK (npk_n IN (0, 1)),
    npk_p NUMBER(1) CHECK (npk_p IN (0, 1)),
    npk_k NUMBER(1) CHECK (npk_k IN (0, 1)),
    CONSTRAINT fk_sensor_cultivo FOREIGN KEY (cultivo_id) 
        REFERENCES cultivos(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_sensor_cultivo ON sensores(cultivo_id);
CREATE INDEX idx_sensor_timestamp ON sensores(timestamp);

-- =============================================
-- TABELA: IRRIGACOES
-- Histórico de decisões de irrigação
-- =============================================
CREATE TABLE irrigacoes (
    id NUMBER(10) PRIMARY KEY,
    cultivo_id NUMBER(10) NOT NULL,
    leitura_id NUMBER(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    acionado NUMBER(1) CHECK (acionado IN (0, 1)),
    motivo VARCHAR2(255) NOT NULL,
    condicao NUMBER(1) CHECK (condicao BETWEEN 1 AND 6),
    CONSTRAINT fk_irrigacao_cultivo FOREIGN KEY (cultivo_id) 
        REFERENCES cultivos(id) ON DELETE CASCADE,
    CONSTRAINT fk_irrigacao_sensor FOREIGN KEY (leitura_id) 
        REFERENCES sensores(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_irrigacao_cultivo ON irrigacoes(cultivo_id);
CREATE INDEX idx_irrigacao_timestamp ON irrigacoes(timestamp);
CREATE INDEX idx_irrigacao_acionado ON irrigacoes(acionado);

-- =============================================
-- TABELA: ESTOQUE
-- Controle de insumos agrícolas
-- =============================================
CREATE TABLE estoque (
    id NUMBER(10) PRIMARY KEY,
    produto VARCHAR2(100) NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    quantidade_kg NUMBER(10,2) CHECK (quantidade_kg >= 0),
    data_compra DATE NOT NULL,
    validade DATE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_estoque_tipo ON estoque(tipo);
CREATE INDEX idx_estoque_validade ON estoque(validade);

-- =============================================
-- SEQUENCES (Auto-incremento de IDs)
-- =============================================
CREATE SEQUENCE seq_cultivos START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_sensores START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_irrigacoes START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_estoque START WITH 1 INCREMENT BY 1;

-- =============================================
-- VIEWS (Consultas úteis)
-- =============================================

-- View: Últimas leituras de cada cultivo
CREATE OR REPLACE VIEW v_ultimas_leituras AS
SELECT c.id AS cultivo_id,
       c.nome AS cultivo_nome,
       s.timestamp,
       s.temperatura,
       s.umidade_solo,
       s.ph,
       s.npk_n,
       s.npk_p,
       s.npk_k
FROM sensores s
INNER JOIN cultivos c ON s.cultivo_id = c.id
WHERE s.timestamp = (
    SELECT MAX(timestamp) 
    FROM sensores 
    WHERE cultivo_id = c.id
);

-- View: Estatísticas de irrigação por cultivo
CREATE OR REPLACE VIEW v_stats_irrigacao AS
SELECT c.id AS cultivo_id,
       c.nome AS cultivo_nome,
       COUNT(i.id) AS total_verificacoes,
       SUM(CASE WHEN i.acionado = 1 THEN 1 ELSE 0 END) AS total_acionadas,
       ROUND(SUM(CASE WHEN i.acionado = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(i.id), 2) AS taxa_acionamento
FROM cultivos c
LEFT JOIN irrigacoes i ON c.id = i.cultivo_id
GROUP BY c.id, c.nome;

-- View: Alertas de estoque
CREATE OR REPLACE VIEW v_alertas_estoque AS
SELECT id,
       produto,
       tipo,
       quantidade_kg,
       validade,
       CASE 
           WHEN validade < SYSDATE THEN 'VENCIDO'
           WHEN validade < SYSDATE + 30 THEN 'VENCIMENTO_PROXIMO'
           WHEN quantidade_kg < 10 THEN 'ESTOQUE_BAIXO'
           ELSE 'OK'
       END AS status_alerta
FROM estoque
WHERE quantidade_kg < 10 OR validade < SYSDATE + 30;

-- =============================================
-- GRANTS (Permissões - ajuste conforme usuários)
-- =============================================
-- GRANT SELECT, INSERT, UPDATE, DELETE ON cultivos TO farmtech_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON sensores TO farmtech_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON irrigacoes TO farmtech_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON estoque TO farmtech_user;

-- =============================================
-- COMMIT
-- =============================================
COMMIT;

-- Mensagem de sucesso
SELECT 'Tabelas criadas com sucesso!' AS status FROM DUAL;
