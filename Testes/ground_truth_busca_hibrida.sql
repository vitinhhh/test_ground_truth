-- ============================================
-- GROUND TRUTH PARA BUSCA HÍBRIDA
-- Estrutura correta: QUERY + RESPOSTAS ESPERADAS
-- ============================================

-- ============================================
-- TABELA 1: QUERIES (Perguntas de busca)
-- ============================================

CREATE TABLE IF NOT EXISTS queries (
    query_id INT PRIMARY KEY AUTO_INCREMENT,
    query_texto VARCHAR(255) NOT NULL,
    descricao VARCHAR(500),
    tipo_busca VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insira as queries de teste
INSERT INTO queries (query_texto, descricao, tipo_busca) VALUES
(1, 'guitarra barata para iniciante', 'Usuário procura guitarra com bom custo-benefício', 'geral'),
(2, 'instrumento caro e profissional', 'Usuário procura instrumento de qualidade premium', 'geral'),
(3, 'acessório barato para guitarra', 'Usuário procura acessório de baixo custo', 'geral'),
(4, 'bateria com estoque baixo', 'Usuário procura bateria (produtos com pouquíssimo estoque)', 'geral'),
(5, 'equipamento de estúdio profissional', 'Usuário procura equipamento para estúdio', 'geral'),
(6, 'teclado sintetizador', 'Usuário procura teclado/sintetizador', 'geral'),
(7, 'produtos de áudio caros', 'Usuário procura produtos de áudio premium', 'geral'),
(8, 'instrumento de sopro de qualidade', 'Usuário procura saxofone, trompete ou similar', 'geral'),
(9, 'acessório de proteção para instrumento', 'Usuário procura capas e estojos', 'geral'),
(10, 'items baratos para iniciante', 'Usuário procura produtos baratos para começar', 'geral');

-- ============================================
-- TABELA 2: GROUND TRUTH (Respostas esperadas)
-- Estrutura: query_id -> lista de produto_ids relevantes
-- ============================================

CREATE TABLE IF NOT EXISTS ground_truth (
    ground_truth_id INT PRIMARY KEY AUTO_INCREMENT,
    query_id INT NOT NULL,
    produto_id INT NOT NULL,
    relevancia_score INT, -- 1 (pouco relevante) a 5 (muito relevante)
    posicao_esperada INT, -- Ordem esperada no ranking
    FOREIGN KEY (query_id) REFERENCES queries(query_id),
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
);

-- ============================================
-- INSERINDO GROUND TRUTH
-- ============================================

-- QUERY 1: "guitarra barata para iniciante"
-- Respostas esperadas: Produto 1 (guitarra), Produto 20 (capo), Produto 11 (violão)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(1, 1, 5, 1),   -- Guitarra Acústica (MUITO relevante)
(1, 11, 4, 2),  -- Violão Clássico (Relevante)
(1, 20, 3, 3);  -- Capotrasto (Pouco relevante)

-- QUERY 2: "instrumento caro e profissional"
-- Respostas esperadas: Produto 21 (saxofone), Produto 38 (viola), Produto 25 (trompete)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(2, 21, 5, 1),  -- Saxofone (MUITO relevante - R$ 4500)
(2, 38, 5, 2),  -- Viola de Arco (MUITO relevante - R$ 2800)
(2, 25, 4, 3);  -- Trompete (Relevante - R$ 1650)

-- QUERY 3: "acessório barato para guitarra"
-- Respostas esperadas: Produto 24 (plectro), Produto 4 (baqueta), Produto 34 (corda)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(3, 24, 5, 1),  -- Plectro (MUITO relevante - R$ 15.50)
(3, 4, 5, 2),   -- Baqueta (MUITO relevante - R$ 25.90)
(3, 34, 4, 3),  -- Corda de Aço (Relevante - R$ 42.00)
(3, 15, 3, 4);  -- Correia (Pouco relevante - R$ 68.00)

-- QUERY 4: "bateria com estoque baixo"
-- Respostas esperadas: Produto 10 (bateria), Produto 17 (accordion)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(4, 10, 5, 1),  -- Bateria (MUITO relevante - estoque 2)
(4, 17, 4, 2),  -- Accordion (Relevante - estoque 1)
(4, 21, 3, 3);  -- Saxofone (Pouco relevante - estoque 1)

-- QUERY 5: "equipamento de estúdio profissional"
-- Respostas esperadas: Produto 14 (interface), Produto 16 (monitor), Produto 28 (gravador)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(5, 16, 5, 1),  -- Monitor Áudio (MUITO relevante - R$ 799)
(5, 14, 5, 2),  -- Interface de Áudio (MUITO relevante - R$ 549)
(5, 28, 4, 3),  -- Gravador Digital (Relevante - R$ 599.90)
(5, 33, 4, 4);  -- Monitor Estéreo (Relevante - R$ 899)

-- QUERY 6: "teclado sintetizador"
-- Respostas esperadas: Produto 5 (teclado)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(6, 5, 5, 1),   -- Teclado Sintetizador (MUITO relevante - exato)
(6, 1, 2, 2),   -- Guitarra (Pouco relevante - similar)
(6, 19, 2, 3);  -- Pad MIDI (Pouco relevante - similar)

-- QUERY 7: "produtos de áudio caros"
-- Respostas esperadas: Produto 16 (monitor), Produto 33 (monitor estéreo), Produto 3 (fone)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(7, 16, 5, 1),  -- Monitor (MUITO relevante - R$ 799)
(7, 33, 5, 2),  -- Monitor Estéreo (MUITO relevante - R$ 899)
(7, 3, 3, 3),   -- Fone (Pouco relevante - R$ 299.90)
(7, 2, 3, 4);   -- Microfone (Pouco relevante - R$ 156.50)

-- QUERY 8: "instrumento de sopro de qualidade"
-- Respostas esperadas: Produto 21 (saxofone), Produto 25 (trompete), Produto 35 (clarinete)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(8, 21, 5, 1),  -- Saxofone (MUITO relevante)
(8, 25, 5, 2),  -- Trompete (MUITO relevante)
(8, 35, 4, 3),  -- Clarinete (Relevante)
(8, 17, 2, 4);  -- Accordion (Pouco relevante)

-- QUERY 9: "acessório de proteção para instrumento"
-- Respostas esperadas: Produto 40 (estojo), Produto 7 (capa), Produto 32 (humidificador)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(9, 40, 5, 1),  -- Estojo Rígido (MUITO relevante - R$ 420)
(9, 7, 5, 2),   -- Capa Protetora (MUITO relevante - R$ 45)
(9, 32, 4, 3),  -- Humidificador (Relevante - R$ 85)
(9, 13, 3, 4);  -- Stand (Pouco relevante - R$ 89.90)

-- QUERY 10: "items baratos para iniciante"
-- Respostas esperadas: Produto 24 (plectro), Produto 4 (baqueta), Produto 37 (almofada fone)
INSERT INTO ground_truth (query_id, produto_id, relevancia_score, posicao_esperada) VALUES
(10, 24, 5, 1), -- Plectro (MUITO relevante - R$ 15.50)
(10, 4, 5, 2),  -- Baqueta (MUITO relevante - R$ 25.90)
(10, 37, 4, 3), -- Almofada Fone (Relevante - R$ 18.90)
(10, 9, 3, 4),  -- Cabo XLR (Pouco relevante - R$ 32.50)
(10, 18, 3, 5); -- Metrônomo (Pouco relevante - R$ 185)

-- ============================================
-- QUERIES PARA CONSULTAR GROUND TRUTH
-- ============================================

-- VER TODOS AS QUERIES
SELECT * FROM queries;

-- VER RESPOSTAS ESPERADAS PARA QUERY 1
SELECT 
    q.query_id,
    q.query_texto,
    gt.produto_id,
    p.nome_produto,
    p.categoria,
    p.preco_unitario,
    gt.relevancia_score,
    gt.posicao_esperada
FROM queries q
LEFT JOIN ground_truth gt ON q.query_id = gt.query_id
LEFT JOIN produtos p ON gt.produto_id = p.produto_id
WHERE q.query_id = 1
ORDER BY gt.posicao_esperada;

-- CONTAR PRODUTOS RELEVANTES POR QUERY
SELECT 
    q.query_id,
    q.query_texto,
    COUNT(gt.produto_id) as total_relevantes,
    AVG(gt.relevancia_score) as relevancia_media
FROM queries q
LEFT JOIN ground_truth gt ON q.query_id = gt.query_id
GROUP BY q.query_id
ORDER BY q.query_id;

-- LISTAR TODOS OS GROUND TRUTHS (Estrutura completa)
SELECT 
    gt.ground_truth_id,
    q.query_id,
    q.query_texto,
    gt.produto_id,
    p.nome_produto,
    p.categoria,
    p.preco_unitario,
    gt.relevancia_score,
    gt.posicao_esperada
FROM ground_truth gt
JOIN queries q ON gt.query_id = q.query_id
JOIN produtos p ON gt.produto_id = p.produto_id
ORDER BY q.query_id, gt.posicao_esperada;

-- ============================================
-- NOTAS IMPORTANTES
-- ============================================

/*
ESTRUTURA CORRETA PARA BUSCA HÍBRIDA:

1. QUERIES (Perguntas de busca)
   - O que o usuário busca
   - Exemplo: "guitarra barata para iniciante"

2. GROUND TRUTH (Respostas esperadas)
   - Quais produtos são relevantes para cada query
   - Score de relevância (1-5)
   - Posição esperada no ranking

3. USO COM MMR/NDCG:
   - Busca Lexical retorna: [1, 11, 20]
   - Busca Semântica retorna: [1, 15, 11]
   - Busca Híbrida retorna: [1, 11, 15]
   - Ground Truth esperado: [1, 11, 20]
   
   Calcula-se MMR ou NDCG para cada tipo de busca
   e compara qual é melhor!

EXEMPLO DE CÁLCULO MMR:
   MMR = (1/1 + 1/2 + 1/3 + 0 + ...) / num_queries
   (onde 0 = não encontrado no ranking esperado)
*/
