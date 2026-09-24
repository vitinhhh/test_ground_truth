

Aqui está como importar o CSV para um banco de dados SQL e testar.

### Pré-requisitos
```bash
# 1. Ter Python 3.8+
python --version

# 2. Instalar MySQL 

# 3. Instalar bibliotecas
pip install mysql-connector-python pandas
```


Abra `02_importar_e_testar.py` e edite:

```python
DB_CONFIG = {
    'host': 'localhost',      # Mude se o MySQL estiver em outro servidor
    'user': 'root',           # Seu usuário MySQL
    'password': '',           # Sua senha MySQL
    'port': 3306,             # Porta padrão (mude se necessário)
}
```

### Executar Script

Na mesma pasta onde estão:
- `02_importar_e_testar.py`
- `dataset_varejo_musical_exemplo.csv`

Execute:
```bash
python 02_importar_e_testar.py
```

### Passo 3: Resultado Esperado

```
============================================================
IMPORTAÇÃO E TESTE DE DATASET
Varejo Online Musical
============================================================

🔌 Conectando ao banco de dados...
✓ Conectado ao MySQL com sucesso!

📦 Criando banco de dados...
✓ Banco 'varejo_musical' criado/validado

📋 Criando tabela 'produtos'...
✓ Tabela 'produtos' criada

📂 Lendo arquivo 'dataset_varejo_musical_exemplo.csv'...
✓ CSV lido com sucesso: 40 linhas

📥 Importando dados para o banco de dados...
✓ 40 produtos importados com sucesso!

🔍 Validando integridade dos dados...

┌─ TESTES DE INTEGRIDADE
│  Total de produtos................... 40 ✓
│  Valores NULL........................ 0 ✓
│  SKU duplicados...................... 0 ✓
│  Preços negativos.................... 0 ✓
│  Estoque negativo.................... 0 ✓
│  Status válido....................... 0 ✓
└─

📊 RELATÓRIOS E ESTATÍSTICAS
============================================================

1️⃣  RESUMO GERAL
   Total de produtos: 40

2️⃣  DISTRIBUIÇÃO POR CATEGORIA
   Instrumentos........................ 10
   Acessórios.......................... 15
   Áudio............................... 15

3️⃣  ANÁLISE DE PREÇOS
   Mínimo:............ R$ 15.50
   Máximo:............ R$ 4500.00
   Média:............. R$ 547.25
   Desvio padrão:..... R$ 1089.32

... [mais relatórios]

✅ IMPORTAÇÃO CONCLUÍDA COM SUCESSO!
```

