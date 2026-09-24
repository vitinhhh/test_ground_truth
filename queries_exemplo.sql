-- 1.1 Listar todos os produtos
SELECT * FROM produtos 
ORDER BY produto_id;

-- 1.2 Produtos com filtro de categoria
SELECT produto_id, nome_produto, categoria, preco_unitario, quantidade_estoque
FROM produtos 
WHERE categoria = 'Instrumentos'
ORDER BY nome_produto;

-- 1.3 Produtos de uma marca específica
SELECT produto_id, nome_produto, artista_marca, preco_unitario
FROM produtos 
WHERE artista_marca = 'Yamaha'
ORDER BY preco_unitario DESC;


-- ============================================
-- 2. CONSULTAS COM ESTOQUE
-- ============================================

-- 2.1 Produtos com estoque baixo (< 5 unidades) - ALERTA
SELECT produto_id, nome_produto, categoria, quantidade_estoque
FROM produtos 
WHERE quantidade_estoque < 5
ORDER BY quantidade_estoque ASC;

-- 2.2 Produtos sem estoque
SELECT produto_id, nome_produto, categoria, artista_marca
FROM produtos 
WHERE quantidade_estoque = 0;

-- 2.3 Produtos com alto estoque (> 50 unidades)
SELECT produto_id, nome_produto, quantidade_estoque, preco_unitario,
       (quantidade_estoque * preco_unitario) AS valor_total
FROM produtos 
WHERE quantidade_estoque > 50
ORDER BY quantidade_estoque DESC;

-- 2.4 Total de unidades em estoque por categoria
SELECT categoria, 
       COUNT(*) AS total_produtos,
       SUM(quantidade_estoque) AS total_unidades,
       AVG(quantidade_estoque) AS media_estoque
FROM produtos 
GROUP BY categoria
ORDER BY total_unidades DESC;


-- ============================================
-- 3. ANÁLISE DE PREÇOS
-- ============================================

-- 3.1 Produtos mais caros
SELECT produto_id, nome_produto, categoria, preco_unitario
FROM produtos 
ORDER BY preco_unitario DESC
LIMIT 10;

-- 3.2 Produtos mais baratos
SELECT produto_id, nome_produto, categoria, preco_unitario
FROM produtos 
ORDER BY preco_unitario ASC
LIMIT 10;

-- 3.3 Preço médio por categoria
SELECT categoria,
       COUNT(*) AS total_produtos,
       AVG(preco_unitario) AS preco_medio,
       MIN(preco_unitario) AS preco_minimo,
       MAX(preco_unitario) AS preco_maximo
FROM produtos 
GROUP BY categoria
ORDER BY preco_medio DESC;

-- 3.4 Variação de preço (desvio padrão)
SELECT categoria,
       AVG(preco_unitario) AS preco_medio,
       STDDEV(preco_unitario) AS desvio_padrao
FROM produtos 
GROUP BY categoria;


-- ============================================
-- 4. ANÁLISE DE VALOR EM ESTOQUE
-- ============================================

-- 4.1 Valor total em estoque (Inventário)
SELECT produto_id, nome_produto, categoria,
       quantidade_estoque,
       preco_unitario,
       (quantidade_estoque * preco_unitario) AS valor_total_estoque
FROM produtos 
WHERE status = 'ativo'
ORDER BY valor_total_estoque DESC;

-- 4.2 Top 10 produtos com maior valor em estoque
SELECT produto_id, nome_produto, artista_marca,
       quantidade_estoque, preco_unitario,
       (quantidade_estoque * preco_unitario) AS valor_investido
FROM produtos 
WHERE status = 'ativo'
ORDER BY valor_investido DESC
LIMIT 10;

-- 4.3 Capital total investido por categoria
SELECT categoria,
       SUM(quantidade_estoque * preco_unitario) AS valor_total_categoria,
       COUNT(*) AS total_produtos,
       AVG(quantidade_estoque * preco_unitario) AS valor_medio_produto
FROM produtos 
WHERE status = 'ativo'
GROUP BY categoria
ORDER BY valor_total_categoria DESC;

-- 4.4 Valor total de todo o inventário
SELECT SUM(quantidade_estoque * preco_unitario) AS valor_total_inventario,
       COUNT(*) AS total_produtos,
       SUM(quantidade_estoque) AS total_unidades
FROM produtos 
WHERE status = 'ativo';


-- ============================================
-- 5. ANÁLISE POR FORNECEDOR
-- ============================================

-- 5.1 Produtos por fornecedor
SELECT fornecedor, 
       COUNT(*) AS total_produtos,
       SUM(quantidade_estoque) AS total_estoque
FROM produtos 
GROUP BY fornecedor
ORDER BY total_produtos DESC;

-- 5.2 Valor investido por fornecedor
SELECT fornecedor,
       COUNT(*) AS total_produtos,
       SUM(quantidade_estoque * preco_unitario) AS valor_total,
       AVG(preco_unitario) AS preco_medio
FROM produtos 
GROUP BY fornecedor
ORDER BY valor_total DESC;

-- 5.3 Fornecedores com produtos em falta
SELECT DISTINCT fornecedor
FROM produtos 
WHERE quantidade_estoque = 0
ORDER BY fornecedor;


-- ============================================
-- 6. ANÁLISE TEMPORAL
-- ============================================

-- 6.1 Produtos atualizados hoje
SELECT produto_id, nome_produto, data_atualizacao
FROM produtos 
WHERE DATE(data_atualizacao) = CURDATE();

-- 6.2 Produtos atualizados nos últimos 7 dias
SELECT produto_id, nome_produto, data_atualizacao
FROM produtos 
WHERE DATE(data_atualizacao) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY data_atualizacao DESC;

-- 6.3 Produtos não atualizados há mais de 30 dias
SELECT produto_id, nome_produto, data_atualizacao
FROM produtos 
WHERE DATE(data_atualizacao) < DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY data_atualizacao ASC;


-- ============================================
-- 7. ANÁLISE DE SKU E CODIFICAÇÃO
-- ============================================

-- 7.1 SKUs por categoria
SELECT categoria, COUNT(*) AS total_skus
FROM produtos 
GROUP BY categoria;

-- 7.2 Validar SKUs duplicados (verificação de integridade)
SELECT sku, COUNT(*) AS ocorrencias
FROM produtos 
GROUP BY sku
HAVING COUNT(*) > 1;

-- 7.3 Produtos sem SKU
SELECT produto_id, nome_produto
FROM produtos 
WHERE sku IS NULL OR sku = '';


-- ============================================
-- 8. ANÁLISE DE STATUS
-- ============================================

-- 8.1 Produtos ativos vs inativos
SELECT status, COUNT(*) AS total
FROM produtos 
GROUP BY status;

-- 8.2 Condicionar inatividade por estoque
SELECT produto_id, nome_produto, quantidade_estoque, status,
       CASE 
           WHEN quantidade_estoque = 0 THEN 'deveria_ser_inativo'
           ELSE 'status_ok'
       END AS status_esperado
FROM produtos;


-- ============================================
-- 9. QUERIES COMPLEXAS (JOIN-READY)
-- ============================================

-- 9.1 Produtos que precisam reposição urgente
-- (Estoque baixo + valor alto = impacto financeiro)
SELECT produto_id, nome_produto, categoria, artista_marca,
       quantidade_estoque, preco_unitario,
       (quantidade_estoque * preco_unitario) AS valor_em_risco
FROM produtos 
WHERE quantidade_estoque < 5 
  AND preco_unitario > 500
  AND status = 'ativo'
ORDER BY valor_em_risco DESC;

-- 9.2 Análise de diversificação por marca
SELECT artista_marca,
       COUNT(*) AS total_produtos,
       COUNT(DISTINCT categoria) AS categorias_cobertas,
       SUM(quantidade_estoque) AS total_unidades
FROM produtos 
GROUP BY artista_marca
ORDER BY total_produtos DESC;

-- 9.3 Produtos "problema" (baixo estoque + alto valor)
SELECT 
    produto_id,
    nome_produto,
    categoria,
    quantidade_estoque,
    preco_unitario,
    (quantidade_estoque * preco_unitario) AS valor_em_risco,
    CASE 
        WHEN quantidade_estoque < 3 AND preco_unitario > 1000 THEN 'CRÍTICO'
        WHEN quantidade_estoque < 5 AND preco_unitario > 500 THEN 'ALTO'
        WHEN quantidade_estoque < 10 THEN 'MÉDIO'
        ELSE 'OK'
    END AS prioridade_reposicao
FROM produtos 
WHERE status = 'ativo'
ORDER BY prioridade_reposicao DESC;


-- ============================================
-- 10. QUERIES PARA TESTES GROUND TRUTH
-- ============================================

-- Essas queries DEVEM retornar resultados específicos
-- Usadas para validar integridade do database

-- 10.1 Contar total exato de produtos
SELECT COUNT(*) AS total_produtos FROM produtos;
-- ESPERADO: 40 (ou conforme gerado)

-- 10.2 Verificar se existem valores NULL
SELECT COUNT(*) AS null_count
FROM produtos 
WHERE produto_id IS NULL 
   OR nome_produto IS NULL 
   OR categoria IS NULL;
-- ESPERADO: 0

-- 10.3 Validar que SKU são únicos
SELECT COUNT(DISTINCT sku) AS sku_unicos
FROM produtos;
-- ESPERADO: igual a total_produtos (40)

-- 10.4 Valor total de inventory
SELECT SUM(quantidade_estoque * preco_unitario) AS valor_total
FROM produtos 
WHERE status = 'ativo';
-- ESPERADO: >R$ 500.000 (aproximadamente)

-- 10.5 Teste de agregação por categoria
SELECT categoria, COUNT(*) AS qtd
FROM produtos 
GROUP BY categoria
HAVING COUNT(*) > 0;
-- ESPERADO: 3 categorias (Instrumentos, Acessórios, Áudio)


-- ============================================
-- 11. QUERIES DE PERFORMANCE (ÍNDICES)
-- ============================================

-- 11.1 Índice para buscas por categoria
CREATE INDEX idx_categoria ON produtos(categoria);

-- 11.2 Índice para buscas por marca
CREATE INDEX idx_marca ON produtos(artista_marca);

-- 11.3 Índice para filtro de estoque
CREATE INDEX idx_estoque ON produtos(quantidade_estoque);

-- 11.4 Índice combinado para análises frequentes
CREATE INDEX idx_categoria_estoque ON produtos(categoria, quantidade_estoque);


-- ============================================
-- 12. VIEWS (OPCIONAL)
-- ============================================

-- 12.1 View: Resumo de Inventário
CREATE VIEW v_resumo_inventario AS
SELECT 
    categoria,
    COUNT(*) AS total_produtos,
    SUM(quantidade_estoque) AS total_unidades,
    SUM(quantidade_estoque * preco_unitario) AS valor_total,
    AVG(preco_unitario) AS preco_medio
FROM produtos 
WHERE status = 'ativo'
GROUP BY categoria;

-- 12.2 View: Produtos Críticos
CREATE VIEW v_produtos_criticos AS
SELECT 
    produto_id,
    nome_produto,
    categoria,
    quantidade_estoque,
    preco_unitario,
    (quantidade_estoque * preco_unitario) AS valor_em_risco
FROM produtos 
WHERE quantidade_estoque < 5 
  AND status = 'ativo'
ORDER BY quantidade_estoque ASC;

-- 12.3 View: Análise por Fornecedor
CREATE VIEW v_analise_fornecedor AS
SELECT 
    fornecedor,
    COUNT(*) AS total_produtos,
    SUM(quantidade_estoque) AS total_estoque,
    SUM(quantidade_estoque * preco_unitario) AS valor_investido
FROM produtos 
GROUP BY fornecedor;


-- ============================================
-- DICAS DE USO
-- ============================================

/*
Para testar este arquivo:

1. MySQL/MariaDB:
   mysql -u usuario -p database < queries_exemplo.sql

2. PostgreSQL:
   psql -U usuario -d database -f queries_exemplo.sql

3. SQLite:
   sqlite3 database.db < queries_exemplo.sql

Para executar queries individuais:
- Copie a query (sem comentários)
- Cole no seu cliente SQL (MySQL Workbench, pgAdmin, etc)
- Execute com Ctrl+Enter ou botão Run

Para validação (Ground Truth):
- Execute as queries 10.1 a 10.5
- Compare resultados esperados com obtidos
- Diferenças indicam problemas na integridade
*/
