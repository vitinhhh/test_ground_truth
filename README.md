# Projeto de Busca Híbrida

## 1. Dependências — instalar primeiro

Antes de executar qualquer script, instale os seguintes componentes.

### 1.1 Python

Recomendado:

```text
Python 3.13+
```

Verifique a instalação:

```bash
python --version
```

### 1.2 Bibliotecas Python

No terminal, dentro da pasta do projeto:

```bash
python -m pip install pandas mysql-connector-python requests sentence-transformers scikit-learn
```

Bibliotecas utilizadas:

* `pandas`
* `mysql-connector-python`
* `requests`
* `sentence-transformers`
* `scikit-learn`

### 1.3 MySQL

É necessário ter o **MySQL Server** instalado e em execução.

Verifique:

```bash
mysql --version
```

Configuração utilizada pelo projeto:

```text
Host: localhost
Porta: 3306
Usuário: root
Senha: vazia
Banco: varejo_musical
```

O banco e a tabela `produtos` são criados pelo script de importação.

> Caso o MySQL esteja configurado com outra senha ou usuário, altere a configuração de conexão nos scripts.

### 1.4 Ollama

É necessário instalar o **Ollama** para executar a validação do Ground Truth com LLM.

Depois da instalação, baixe o modelo utilizado pelo projeto:

```bash
ollama pull llama3.2:3b
```

Verifique:

```bash
ollama list
```

O modelo utilizado é:

```text
llama3.2:3b
```

O Ollama deve estar em execução para realizar a validação.

---

# 2. Ordem de execução

Depois de instalar todas as dependências, siga esta ordem.

### 2.1 Importar o dataset

```bash
python Scripts/03_importar_dataset.py
```

Esse script cria/configura o banco `varejo_musical` e importa o dataset:

```text
Scripts/dataset_robusto_500produtos.csv
```

---

### 2.2 Executar busca lexical

```bash
python Scripts/04_busca_lexical.py
```

---

### 2.3 Executar busca semântica

```bash
python Scripts/05_busca_semantica.py
```

Na primeira execução, o `sentence-transformers` poderá baixar automaticamente o modelo:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

---

### 2.4 Executar busca híbrida

```bash
python Scripts/06_busca_hibrida.py
```

A busca híbrida combina os resultados da busca lexical e semântica.

---

### 2.5 Validar o Ground Truth com LLM

```bash
python Scripts/08_validar_ground_truth_llm.py
```

Esse processo utiliza:

```text
llama3.2:3b
```

através do Ollama.

O resultado será gerado em:

```text
Testes/ground_truth_validado_llm.csv
```

Esse arquivo é gerado localmente e não faz parte do repositório.

---

### 2.6 Executar as métricas

```bash
python Scripts/07_metricas.py
```

O script calcula:

* MRR
* NDCG@5
* Precision@5
* Recall@5

para as buscas:

* Lexical
* Semântica
* Híbrida

---

# 3. Ground Truth

O Ground Truth utilizado pelo projeto está em:

```text
Testes/ground_truth.csv
```

Ele contém as consultas e os produtos utilizados como referência para a avaliação das buscas.

O arquivo:

```text
Testes/ground_truth_validado_llm.csv
```

não é fornecido pronto no repositório.

Ele deve ser **gerado novamente** executando:

```bash
python Scripts/08_validar_ground_truth_llm.py
```

Dessa forma, a validação realizada pela LLM pode ser reproduzida por outros integrantes do projeto.

---

# 4. Dataset

O dataset atual está em:

```text
Scripts/dataset_robusto_500produtos.csv
```

Ele contém 500 produtos.

As colunas esperadas são:

```text
produto_id
nome_produto
categoria
marca
descricao_longa
preco_unitario
quantidade_estoque
rating
num_reviews
reviews
tags
especificacoes
fornecedor
sku
status
data_adicao
```

Para importar novamente o dataset:

```bash
python Scripts/03_importar_dataset.py
```

---

# 5. Estrutura do projeto

```text
├── Scripts/
│   ├── 03_importar_dataset.py
│   ├── 04_busca_lexical.py
│   ├── 05_busca_semantica.py
│   ├── 06_busca_hibrida.py
│   ├── 07_metricas.py
│   ├── 08_validar_ground_truth_llm.py
│   ├── gerar_dataset_robusto.py
│   └── dataset_robusto_500produtos.csv
│
├── Teste_llm/
│   └── teste_prompt.py
│
├── Testes/
│   ├── ground_truth.csv
│   └── ground_truth_busca_hibrida.sql
│
├── .gitignore
└── README.md
```

---

# 6. Modelo de embeddings

A busca semântica utiliza:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

O modelo é carregado automaticamente pelo `sentence-transformers`.

---

# 7. Busca híbrida

A busca híbrida combina:

```text
Busca lexical
+
Busca semântica
```

Os resultados das duas abordagens são combinados para gerar o ranking final.

---

# 8. Métricas

O projeto utiliza:

```text
MRR
NDCG@5
Precision@5
Recall@5
```

As métricas são calculadas pelo:

```text
Scripts/07_metricas.py
```

---

# 9. Substituição do dataset

É possível utilizar outro dataset, desde que ele mantenha as colunas esperadas pelo sistema.

Após substituir o arquivo:

```text
Scripts/dataset_robusto_500produtos.csv
```

execute novamente:

```bash
python Scripts/03_importar_dataset.py
```

Os métodos de busca passarão a utilizar os novos produtos.

**Importante:** se os produtos forem alterados, o Ground Truth também deverá ser revisado, pois ele está relacionado aos produtos utilizados na avaliação atual.
