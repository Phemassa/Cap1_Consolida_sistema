-- ============================================
-- FarmTech Solutions - Dados Iniciais (Seed)
-- Insere dados de exemplo para testes
-- ============================================

-- =============================================
-- CULTIVOS DE EXEMPLO
-- =============================================
INSERT INTO cultivos (id, nome, cultura_tipo, area_hectares, data_plantio, 
                     nitrogenio_req, fosforo_req, potassio_req, ph_ideal, umidade_ideal)
VALUES (1, 'Banana Prata Lote A', 'BANANA', 5.5, TO_DATE('2025-08-15', 'YYYY-MM-DD'),
        15.0, 10.0, 20.0, 6.5, 60.0);

INSERT INTO cultivos (id, nome, cultura_tipo, area_hectares, data_plantio, 
                     nitrogenio_req, fosforo_req, potassio_req, ph_ideal, umidade_ideal)
VALUES (2, 'Milho Híbrido BRS 2024', 'MILHO', 12.0, TO_DATE('2025-09-01', 'YYYY-MM-DD'),
        12.0, 8.0, 10.0, 6.0, 55.0);

INSERT INTO cultivos (id, nome, cultura_tipo, area_hectares, data_plantio, 
                     nitrogenio_req, fosforo_req, potassio_req, ph_ideal, umidade_ideal)
VALUES (3, 'Banana Nanica Lote B', 'BANANA', 3.2, TO_DATE('2025-07-20', 'YYYY-MM-DD'),
        15.0, 10.0, 20.0, 6.8, 62.0);

-- =============================================
-- LEITURAS DE SENSORES DE EXEMPLO
-- =============================================

-- Leituras para Banana Prata (cultivo_id=1)
-- Cenário: Solo seco, precisa irrigação
INSERT INTO sensores (id, cultivo_id, timestamp, temperatura, umidade_ar, umidade_solo, ph, npk_n, npk_p, npk_k)
VALUES (1, 1, TO_TIMESTAMP('2025-10-11 08:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        26.5, 50.0, 40.0, 6.3, 1, 1, 0);

INSERT INTO sensores (id, cultivo_id, timestamp, temperatura, umidade_ar, umidade_solo, ph, npk_n, npk_p, npk_k)
VALUES (2, 1, TO_TIMESTAMP('2025-10-11 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        28.0, 45.0, 36.0, 6.2, 1, 1, 0);

-- Leituras para Milho (cultivo_id=2)
-- Cenário: Condições ideais
INSERT INTO sensores (id, cultivo_id, timestamp, temperatura, umidade_ar, umidade_solo, ph, npk_n, npk_p, npk_k)
VALUES (3, 2, TO_TIMESTAMP('2025-10-11 08:30:00', 'YYYY-MM-DD HH24:MI:SS'),
        24.0, 75.0, 60.0, 6.5, 1, 1, 1);

INSERT INTO sensores (id, cultivo_id, timestamp, temperatura, umidade_ar, umidade_solo, ph, npk_n, npk_p, npk_k)
VALUES (4, 2, TO_TIMESTAMP('2025-10-11 10:30:00', 'YYYY-MM-DD HH24:MI:SS'),
        25.5, 78.0, 62.4, 6.6, 1, 1, 1);

-- Leituras para Banana Nanica (cultivo_id=3)
-- Cenário: Temperatura alta, umidade baixa
INSERT INTO sensores (id, cultivo_id, timestamp, temperatura, umidade_ar, umidade_solo, ph, npk_n, npk_p, npk_k)
VALUES (5, 3, TO_TIMESTAMP('2025-10-11 14:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        32.0, 40.0, 32.0, 6.0, 1, 1, 1);

-- =============================================
-- HISTÓRICO DE IRRIGAÇÕES DE EXEMPLO
-- =============================================

-- Irrigação acionada: Banana Prata - Solo seco
INSERT INTO irrigacoes (id, cultivo_id, leitura_id, timestamp, acionado, motivo, condicao)
VALUES (1, 1, 1, TO_TIMESTAMP('2025-10-11 08:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'Umidade crítica (40.0%) < 40%', 1);

INSERT INTO irrigacoes (id, cultivo_id, leitura_id, timestamp, acionado, motivo, condicao)
VALUES (2, 1, 2, TO_TIMESTAMP('2025-10-11 10:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'Umidade crítica (36.0%) < 40%', 1);

-- Irrigação NÃO acionada: Milho - Condições ideais
INSERT INTO irrigacoes (id, cultivo_id, leitura_id, timestamp, acionado, motivo, condicao)
VALUES (3, 2, 3, TO_TIMESTAMP('2025-10-11 08:35:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'Condições ótimas - irrigação desnecessária', 6);

INSERT INTO irrigacoes (id, cultivo_id, leitura_id, timestamp, acionado, motivo, condicao)
VALUES (4, 2, 4, TO_TIMESTAMP('2025-10-11 10:35:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'Condições ótimas - irrigação desnecessária', 6);

-- Irrigação acionada: Banana Nanica - Temperatura alta
INSERT INTO irrigacoes (id, cultivo_id, leitura_id, timestamp, acionado, motivo, condicao)
VALUES (5, 3, 5, TO_TIMESTAMP('2025-10-11 14:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'Temperatura alta (32.0°C) > 30°C + umidade 32.0% < 60%', 5);

-- =============================================
-- ESTOQUE DE INSUMOS DE EXEMPLO
-- =============================================

-- Fertilizantes
INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (1, 'Ureia (45% N)', 'fertilizante', 500.0, 
        TO_DATE('2025-09-01', 'YYYY-MM-DD'), TO_DATE('2026-09-01', 'YYYY-MM-DD'));

INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (2, 'Superfosfato Simples (18% P)', 'fertilizante', 300.0,
        TO_DATE('2025-09-10', 'YYYY-MM-DD'), TO_DATE('2027-09-10', 'YYYY-MM-DD'));

INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (3, 'Cloreto de Potássio (60% K)', 'fertilizante', 250.0,
        TO_DATE('2025-09-15', 'YYYY-MM-DD'), TO_DATE('2027-03-15', 'YYYY-MM-DD'));

-- Defensivos
INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (4, 'Fungicida Triazol', 'defensivo', 15.0,
        TO_DATE('2025-08-20', 'YYYY-MM-DD'), TO_DATE('2026-02-20', 'YYYY-MM-DD'));

-- Sementes
INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (5, 'Sementes Milho Híbrido', 'sementes', 80.0,
        TO_DATE('2025-08-01', 'YYYY-MM-DD'), TO_DATE('2026-08-01', 'YYYY-MM-DD'));

-- Produto com estoque baixo (para testar alerta)
INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (6, 'Calcário Dolomítico', 'corretivo', 8.5,
        TO_DATE('2025-07-10', 'YYYY-MM-DD'), TO_DATE('2030-07-10', 'YYYY-MM-DD'));

-- Produto com vencimento próximo (para testar alerta)
INSERT INTO estoque (id, produto, tipo, quantidade_kg, data_compra, validade)
VALUES (7, 'Herbicida Glifosato', 'defensivo', 25.0,
        TO_DATE('2024-11-01', 'YYYY-MM-DD'), TO_DATE('2025-11-01', 'YYYY-MM-DD'));

-- =============================================
-- ATUALIZAR SEQUENCES
-- =============================================
ALTER SEQUENCE seq_cultivos INCREMENT BY 1;
ALTER SEQUENCE seq_sensores INCREMENT BY 1;
ALTER SEQUENCE seq_irrigacoes INCREMENT BY 1;
ALTER SEQUENCE seq_estoque INCREMENT BY 1;

-- Avança sequences para próximo ID disponível
SELECT seq_cultivos.NEXTVAL FROM DUAL;
SELECT seq_sensores.NEXTVAL FROM DUAL;
SELECT seq_irrigacoes.NEXTVAL FROM DUAL;
SELECT seq_estoque.NEXTVAL FROM DUAL;

-- =============================================
-- COMMIT
-- =============================================
COMMIT;

-- Mensagem de sucesso
SELECT 'Dados iniciais inseridos com sucesso!' AS status FROM DUAL;

-- =============================================
-- QUERIES DE VERIFICAÇÃO
-- =============================================

-- Ver cultivos cadastrados
SELECT * FROM cultivos;

-- Ver últimas leituras
SELECT * FROM v_ultimas_leituras;

-- Ver estatísticas de irrigação
SELECT * FROM v_stats_irrigacao;

-- Ver alertas de estoque
SELECT * FROM v_alertas_estoque;
