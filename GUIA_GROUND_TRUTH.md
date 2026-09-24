---

## 📊 Você tem 2 arquivos Ground Truth
### - - - Use o 'queries_exemplo.sql' para testar o Ground Truth - - -

### 1️⃣ **ground_truth_exemplo.csv** (10 testes)

- Básico
- Cobre os pontos principais
- Bom para TCC

### 2️⃣ **ground_truth_expandido.csv** (20 testes) ← NOVO!
- Mais completo
- Testa mais cenários
- Melhor cobertura
- Recomendado usar ESTE

---

## 🎯 Como Abrir e Visualizar 

### OPÇÃO 1: Excel 

1. Clique direito no arquivo `ground_truth_expandido.csv`
2. "Abrir com" → **Excel**
3. Pronto! Fica bonitão em colunas ✅

```
┌───┬─────────────────────────┬──────────────┬────────┬────────────┐
│ID │ Nome                    │ Categoria    │ Preço  │ Estoque    │
├───┼─────────────────────────┼──────────────┼────────┼────────────┤
│1  │ Guitarra Acústica       │ Instrumentos │189.90  │ 15         │
│5  │ Teclado Sintetizador    │ Instrumentos │1850.00 │ 3          │
│10 │ Bateria Acústica        │ Instrumentos │2450.00 │ 2          │
│... (mais 17 testes)
└───┴─────────────────────────┴──────────────┴────────┴────────────┘
```

### OPÇÃO 2: phpMyAdmin 

1. Abra: `http://localhost/phpmyadmin`
2. Banco: `varejo_musical`
3. Copie/cole as queries que vou mostrar

---

## 🧪 Como Testar (20 Testes Rápidos)

Cada linha do arquivo Ground Truth é um **caso de teste**.

**Estrutura:**

```
produto_id → ID do produto a testar
nome_produto → Nome esperado
categoria → Categoria esperada
preco_unitario → Preço esperado
quantidade_estoque → Estoque esperado
status → Status esperado
descricao_teste → O que está sendo testado
```

---

## ✅ Exemplo Prático (Como Testar)

### Teste 1: Produto ID 1 (Guitarra Acústica)

**Query SQL:**
```sql
SELECT 
    produto_id,
    nome_produto,
    categoria,
    preco_unitario,
    quantidade_estoque,
    status
FROM produtos 
WHERE produto_id = 1;
```

**Resultado esperado (Ground Truth):**
```
ID: 1
Nome: Guitarra Acústica 41 Polegadas
Categoria: Instrumentos
Preço: 189.90
Estoque: 15
Status: ativo
```

**O que comparar:**
- Resultado da query = Ground Truth? 
- SIM ✅ → Teste passou!
- NÃO ❌ → Algo está errado

---

- - - Use o 'queries_exemplo.sql' para testar o Ground Truth - - -