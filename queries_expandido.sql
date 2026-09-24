-- ============================================
-- TESTE 1: Produto mais barato (ID 24)
-- Esperado: Plectro, R$ 15.50, 100 unidades
-- ============================================
SELECT * FROM produtos WHERE produto_id = 24;


-- ============================================
-- TESTE 2: Produto mais caro (ID 21)
-- Esperado: Saxofone, R$ 4500.00, 1 unidade
-- ============================================
SELECT * FROM produtos WHERE produto_id = 21;


-- ============================================
-- TESTE 3: Instrumento caro com estoque baixo (ID 5)
-- Esperado: Teclado Sintetizador, R$ 1850.00, 3 unidades
-- ============================================
SELECT * FROM produtos WHERE produto_id = 5;


-- ============================================
-- TESTE 4: Produtos com estoque crítico (< 3 unidades)
-- Esperado: 4 produtos
-- ============================================
SELECT COUNT(*) as total_estoque_critico FROM produtos WHERE quantidade_estoque < 3;


-- ============================================
-- TESTE 5: Total de produtos Acessórios
-- Esperado: 18 produtos
-- ============================================
SELECT COUNT(*) as total_acessorios FROM produtos WHERE categoria = 'Acessórios';


-- ============================================
-- TESTE 6: Produtos com preço > R$ 1000
-- Esperado: 9 produtos
-- ============================================
SELECT COUNT(*) as total_preco_alto FROM produtos WHERE preco_unitario > 1000;


-- ============================================
-- TESTE 7: Valor total em estoque
-- Esperado: R$ 102.464,10
-- ============================================
SELECT ROUND(SUM(quantidade_estoque * preco_unitario), 2) as valor_total_estoque
FROM produtos;


-- ============================================
-- TESTE 8: Bateria Acústica (ID 10) - Estoque crítico
-- Esperado: R$ 2450.00, 2 unidades
-- ============================================
SELECT * FROM produtos WHERE produto_id = 10;


-- ============================================
-- TESTE 9: Equipamentos profissionais caros (> R$ 500)
-- Esperado: 7 produtos
-- ============================================
SELECT COUNT(*) as total_equipamentos_caros 
FROM produtos 
WHERE categoria = 'Equipamentos' AND preco_unitario > 500;


-- ============================================
-- TESTE 10: Total de produtos por categoria
-- Esperado: Acessórios 18, Instrumentos 10, Equipamentos 10, Áudio 2
-- ============================================
SELECT categoria, COUNT(*) as total
FROM produtos
GROUP BY categoria
ORDER BY total DESC;


-- ============================================
-- TESTE 11: Total de fornecedores únicos
-- Esperado: 40 fornecedores
-- ============================================
SELECT COUNT(DISTINCT fornecedor) as total_fornecedores
FROM produtos;


-- ============================================
-- TESTE 12: Produtos com status ativo
-- Esperado: 40
-- ============================================
SELECT COUNT(*) as total_ativos FROM produtos WHERE status = 'ativo';


-- ============================================
-- TESTE 13: Viola de Arco (ID 38) - Instrumento clássico muito caro
-- Esperado: R$ 2800.00, 1 unidade
-- ============================================
SELECT * FROM produtos WHERE produto_id = 38;


-- ============================================
-- TESTE 14: Estoque máximo
-- Esperado: 100
-- ============================================
SELECT MAX(quantidade_estoque) as estoque_maximo FROM produtos;


-- ============================================
-- TESTE 15: Preço médio de Acessórios
-- Esperado: Aproximadamente R$ 150
-- ============================================
SELECT ROUND(AVG(preco_unitario), 2) as preco_medio_acessorios
FROM produtos
WHERE categoria = 'Acessórios';


-- ============================================
-- TESTE 16: Total de produtos categoria Áudio
-- Esperado: 2 produtos
-- ============================================
SELECT COUNT(*) as total_audio FROM produtos WHERE categoria = 'Áudio';


-- ============================================
-- TESTE 17: SKU únicos (todos devem ser diferentes)
-- Esperado: 40 (igual ao total de produtos)
-- ============================================
SELECT COUNT(DISTINCT sku) as sku_unicos FROM produtos;


-- ============================================
-- TESTE 18: Produtos com ID entre 30-40
-- Esperado: 11 produtos
-- ============================================
SELECT COUNT(*) as total_range FROM produtos WHERE produto_id BETWEEN 30 AND 40;


-- ============================================
-- TESTE 19: Produtos marca Yamaha
-- Esperado: 4 produtos
-- ============================================
SELECT COUNT(*) as total_yamaha FROM produtos WHERE artista_marca = 'Yamaha';


-- ============================================
-- TESTE 20: Produtos com preço > R$ 1500
-- Esperado: 6 produtos
-- ============================================
SELECT COUNT(*) as total_preco_muito_alto FROM produtos WHERE preco_unitario > 1500;


-- ============================================
-- BÔNUS: QUERIES ÚTEIS PARA ANÁLISE
-- ============================================

-- BÔNUS 1: Top 5 produtos mais caros
SELECT produto_id, nome_produto, preco_unitario
FROM produtos
ORDER BY preco_unitario DESC
LIMIT 5;

-- BÔNUS 2: Produtos com estoque baixo (alerta)
SELECT produto_id, nome_produto, quantidade_estoque, preco_unitario
FROM produtos
WHERE quantidade_estoque < 5
ORDER BY quantidade_estoque ASC;

-- BÔNUS 3: Valor investido por categoria
SELECT categoria,
       COUNT(*) as total_produtos,
       SUM(quantidade_estoque * preco_unitario) as valor_investido
FROM produtos
GROUP BY categoria
ORDER BY valor_investido DESC;

-- BÔNUS 4: Produtos com maior valor em estoque
SELECT produto_id, nome_produto,
       quantidade_estoque, preco_unitario,
       (quantidade_estoque * preco_unitario) as valor_total
FROM produtos
ORDER BY valor_total DESC
LIMIT 10;

-- BÔNUS 5: Relatório completo por fornecedor
SELECT fornecedor,
       COUNT(*) as total_produtos,
       SUM(quantidade_estoque) as total_estoque,
       ROUND(SUM(quantidade_estoque * preco_unitario), 2) as valor_investido
FROM produtos
GROUP BY fornecedor
ORDER BY valor_investido DESC;

-- ============================================
-- RESUMO DOS TESTES
-- ============================================
-- Total de testes: 20 (principais)
-- Total de queries bônus: 5 (análise extra)
-- Tempo estimado: 15 minutos
--
-- VALIDAÇÃO:
-- Se todos os 20 testes darem resultados esperados
-- → Ground Truth 100% validado ✅
--
-- ============================================
