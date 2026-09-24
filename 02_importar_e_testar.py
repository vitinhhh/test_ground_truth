#!/usr/bin/env python3
"""
Script Python para importar Dataset em Banco de Dados e Testar

Este script automatiza:
1. Cria conexão com banco de dados
2. Cria a tabela 'produtos'
3. Importa dados do CSV
4. Valida integridade dos dados
5. Roda testes (Ground Truth)
6. Mostra relatórios

Requisitos:
    pip install mysql-connector-python pandas
    
Compatível com: MySQL, MariaDB

Uso:
    python 02_importar_e_testar.py
"""

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import sys
from datetime import datetime

# ============================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================

DB_CONFIG = {
    'host': 'localhost',      # Mude se necessário
    'user': 'root',           # Seu usuário MySQL
    'password': '',           # Sua senha MySQL
    'port': 3306,             # Porta padrão MySQL
}

DATABASE_NAME = 'varejo_musical'
CSV_FILE = 'dataset_varejo_musical_exemplo.csv'  # Nome do seu CSV

# ============================================
# ESQUEMA DA TABELA
# ============================================

CREATE_DATABASE = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};
"""

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS produtos (
    produto_id INT PRIMARY KEY AUTO_INCREMENT,
    nome_produto VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    artista_marca VARCHAR(100) NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    quantidade_estoque INT NOT NULL,
    data_atualizacao DATE NOT NULL,
    fornecedor VARCHAR(100) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ativo',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_categoria (categoria),
    INDEX idx_marca (artista_marca),
    INDEX idx_estoque (quantidade_estoque),
    INDEX idx_fornecedor (fornecedor),
    INDEX idx_sku (sku)
);
"""

# ============================================
# FUNÇÕES PRINCIPAIS
# ============================================

def conectar_banco(config):
    """Conecta ao MySQL"""
    try:
        conn = mysql.connector.connect(**config)
        print("✓ Conectado ao MySQL com sucesso!")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("✗ Erro: Usuário ou senha incorretos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("✗ Erro: Banco de dados não existe")
        else:
            print(f"✗ Erro ao conectar: {err}")
        sys.exit(1)


def criar_banco(conn, cursor):
    """Cria o banco de dados"""
    print("\n📦 Criando banco de dados...")
    try:
        cursor.execute(CREATE_DATABASE)
        conn.commit()
        print(f"✓ Banco '{DATABASE_NAME}' criado/validado")
    except mysql.connector.Error as err:
        print(f"✗ Erro ao criar banco: {err}")
        sys.exit(1)


def usar_banco(conn, cursor):
    """Seleciona o banco"""
    cursor.execute(f"USE {DATABASE_NAME}")
    conn.commit()


def criar_tabela(conn, cursor):
    """Cria a tabela produtos"""
    print("\n📋 Criando tabela 'produtos'...")
    try:
        cursor.execute("DROP TABLE IF EXISTS produtos")
        cursor.execute(CREATE_TABLE)
        conn.commit()
        print("✓ Tabela 'produtos' criada")
    except mysql.connector.Error as err:
        print(f"✗ Erro ao criar tabela: {err}")
        sys.exit(1)


def ler_csv(arquivo):
    """Lê o arquivo CSV com Pandas"""
    print(f"\n📂 Lendo arquivo '{arquivo}'...")
    try:
        df = pd.read_csv(arquivo)
        print(f"✓ CSV lido com sucesso: {len(df)} linhas")
        return df
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{arquivo}' não encontrado")
        print(f"   Verifique se o arquivo está na mesma pasta que o script")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Erro ao ler CSV: {e}")
        sys.exit(1)


def importar_csv(conn, cursor, df):
    """Importa dados do DataFrame para o banco"""
    print("\n📥 Importando dados para o banco de dados...")
    
    try:
        for index, row in df.iterrows():
            sql = """
            INSERT INTO produtos 
            (nome_produto, categoria, artista_marca, preco_unitario, 
             quantidade_estoque, data_atualizacao, fornecedor, sku, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                row['nome_produto'],
                row['categoria'],
                row['artista_marca'],
                row['preco_unitario'],
                row['quantidade_estoque'],
                row['data_atualizacao'],
                row['fornecedor'],
                row['sku'],
                row['status']
            )
            
            cursor.execute(sql, values)
        
        conn.commit()
        print(f"✓ {len(df)} produtos importados com sucesso!")
        
    except mysql.connector.Error as err:
        print(f"✗ Erro ao importar: {err}")
        conn.rollback()
        sys.exit(1)


def validar_dados(cursor):
    """Valida integridade dos dados"""
    print("\n🔍 Validando integridade dos dados...")
    
    testes = []
    
    # Teste 1: Contar registros
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]
    testes.append(("Total de produtos", total, f"{total} ✓"))
    
    # Teste 2: Verificar NULLs
    cursor.execute("""
    SELECT COUNT(*) FROM produtos 
    WHERE nome_produto IS NULL OR categoria IS NULL OR sku IS NULL
    """)
    nulls = cursor.fetchone()[0]
    testes.append(("Valores NULL", nulls, "0 ✓" if nulls == 0 else f"{nulls} ✗"))
    
    # Teste 3: SKU duplicados
    cursor.execute("""
    SELECT COUNT(*) FROM (
        SELECT sku FROM produtos GROUP BY sku HAVING COUNT(*) > 1
    ) as duplicados
    """)
    duplicados = cursor.fetchone()[0]
    testes.append(("SKU duplicados", duplicados, "0 ✓" if duplicados == 0 else f"{duplicados} ✗"))
    
    # Teste 4: Preços negativos
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE preco_unitario < 0")
    negativos = cursor.fetchone()[0]
    testes.append(("Preços negativos", negativos, "0 ✓" if negativos == 0 else f"{negativos} ✗"))
    
    # Teste 5: Estoque negativo
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE quantidade_estoque < 0")
    est_neg = cursor.fetchone()[0]
    testes.append(("Estoque negativo", est_neg, "0 ✓" if est_neg == 0 else f"{est_neg} ✗"))
    
    # Teste 6: Status válido
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE status NOT IN ('ativo', 'inativo')")
    status_invalido = cursor.fetchone()[0]
    testes.append(("Status válido", status_invalido, "0 ✓" if status_invalido == 0 else f"{status_invalido} ✗"))
    
    print("\n┌─ TESTES DE INTEGRIDADE")
    for teste, valor, resultado in testes:
        print(f"│  {teste:.<30} {resultado}")
    print("└─")
    
    return all("✓" in resultado for _, _, resultado in testes)


def gerar_relatorios(cursor):
    """Gera relatórios estatísticos"""
    print("\n📊 RELATÓRIOS E ESTATÍSTICAS")
    print("=" * 60)
    
    # 1. Total de produtos
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]
    print(f"\n1️⃣  RESUMO GERAL")
    print(f"   Total de produtos: {total}")
    
    # 2. Por categoria
    print(f"\n2️⃣  DISTRIBUIÇÃO POR CATEGORIA")
    cursor.execute("""
    SELECT categoria, COUNT(*) as total
    FROM produtos
    GROUP BY categoria
    ORDER BY total DESC
    """)
    for categoria, count in cursor.fetchall():
        print(f"   {categoria:.<30} {count}")
    
    # 3. Preços
    print(f"\n3️⃣  ANÁLISE DE PREÇOS")
    cursor.execute("""
    SELECT 
        MIN(preco_unitario) as minimo,
        MAX(preco_unitario) as maximo,
        ROUND(AVG(preco_unitario), 2) as media,
        ROUND(STDDEV(preco_unitario), 2) as desvio
    FROM produtos
    """)
    minimo, maximo, media, desvio = cursor.fetchone()
    print(f"   Mínimo:............ R$ {minimo:.2f}")
    print(f"   Máximo:............ R$ {maximo:.2f}")
    print(f"   Média:............. R$ {media:.2f}")
    print(f"   Desvio padrão:..... R$ {desvio:.2f}")
    
    # 4. Estoque
    print(f"\n4️⃣  ANÁLISE DE ESTOQUE")
    cursor.execute("""
    SELECT 
        SUM(quantidade_estoque) as total,
        MIN(quantidade_estoque) as minimo,
        MAX(quantidade_estoque) as maximo,
        ROUND(AVG(quantidade_estoque), 2) as media
    FROM produtos
    """)
    total_est, min_est, max_est, media_est = cursor.fetchone()
    print(f"   Total de unidades:. {total_est}")
    print(f"   Mínimo por produto: {min_est}")
    print(f"   Máximo por produto: {max_est}")
    print(f"   Média por produto:. {media_est}")
    
    # 5. Valor em estoque
    print(f"\n5️⃣  VALOR TOTAL EM ESTOQUE")
    cursor.execute("""
    SELECT 
        ROUND(SUM(quantidade_estoque * preco_unitario), 2) as valor_total
    FROM produtos
    """)
    valor_total = cursor.fetchone()[0]
    print(f"   R$ {valor_total:,.2f}")
    
    # 6. Por fornecedor
    print(f"\n6️⃣  FORNECEDORES")
    cursor.execute("""
    SELECT fornecedor, COUNT(*) as total
    FROM produtos
    GROUP BY fornecedor
    ORDER BY total DESC
    """)
    for fornecedor, count in cursor.fetchall():
        print(f"   {fornecedor:.<30} {count} produtos")
    
    # 7. Produtos com estoque baixo
    print(f"\n7️⃣  PRODUTOS COM ESTOQUE BAIXO (< 5)")
    cursor.execute("""
    SELECT produto_id, nome_produto, quantidade_estoque
    FROM produtos
    WHERE quantidade_estoque < 5
    ORDER BY quantidade_estoque ASC
    """)
    baixo_estoque = cursor.fetchall()
    if baixo_estoque:
        for pid, nome, est in baixo_estoque:
            print(f"   ID {pid}: {nome:.<35} {est} unidades")
    else:
        print(f"   ✓ Nenhum produto com estoque baixo")
    
    print("\n" + "=" * 60)


def testar_ground_truth(cursor):
    """Testa Ground Truth (validações específicas)"""
    print("\n✅ TESTES GROUND TRUTH (VALIDAÇÕES)")
    print("=" * 60)
    
    # Teste 1
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE categoria = 'Instrumentos'")
    instrumentos = cursor.fetchone()[0]
    print(f"Produtos da categoria 'Instrumentos': {instrumentos}")
    
    # Teste 2
    cursor.execute("""
    SELECT COUNT(*) FROM produtos 
    WHERE quantidade_estoque > 50
    """)
    alto_estoque = cursor.fetchone()[0]
    print(f"Produtos com estoque > 50: {alto_estoque}")
    
    # Teste 3
    cursor.execute("""
    SELECT COUNT(*) FROM produtos 
    WHERE preco_unitario > 1000
    """)
    caros = cursor.fetchone()[0]
    print(f"Produtos com preço > R$ 1.000: {caros}")
    
    # Teste 4
    cursor.execute("""
    SELECT COUNT(*) FROM produtos WHERE status = 'ativo'
    """)
    ativos = cursor.fetchone()[0]
    print(f"Produtos com status 'ativo': {ativos}")
    
    # Teste 5: Produto específico
    cursor.execute("""
    SELECT nome_produto, preco_unitario, quantidade_estoque
    FROM produtos
    WHERE produto_id = 1
    """)
    resultado = cursor.fetchone()
    if resultado:
        nome, preco, est = resultado
        print(f"Produto ID 1: {nome} | R$ {preco} | {est} unidades")
    
    print("=" * 60)


def salvar_relatorio(cursor, arquivo_saida='relatorio_importacao.txt'):
    """Salva relatório em arquivo"""
    print(f"\n💾 Salvando relatório em '{arquivo_saida}'...")
    
    try:
        with open(arquivo_saida, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("RELATÓRIO DE IMPORTAÇÃO DO DATASET\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Estatísticas
            cursor.execute("SELECT COUNT(*) FROM produtos")
            f.write(f"Total de produtos: {cursor.fetchone()[0]}\n")
            
            cursor.execute("""
            SELECT 
                SUM(quantidade_estoque) as total_est,
                ROUND(SUM(quantidade_estoque * preco_unitario), 2) as valor_total,
                COUNT(DISTINCT categoria) as categorias,
                COUNT(DISTINCT fornecedor) as fornecedores
            FROM produtos
            """)
            total_est, valor, cats, forn = cursor.fetchone()
            f.write(f"Total de unidades em estoque: {total_est}\n")
            f.write(f"Valor total em estoque: R$ {valor:,.2f}\n")
            f.write(f"Categorias: {cats}\n")
            f.write(f"Fornecedores: {forn}\n")
            
            # Categorias
            f.write("\n\nDISTRIBUIÇÃO POR CATEGORIA:\n")
            cursor.execute("""
            SELECT categoria, COUNT(*) as total
            FROM produtos GROUP BY categoria ORDER BY total DESC
            """)
            for cat, total in cursor.fetchall():
                f.write(f"  {cat}: {total}\n")
            
            f.write("\n\nIMPORTAÇÃO CONCLUÍDA COM SUCESSO! ✓\n")
        
        print(f"✓ Relatório salvo em '{arquivo_saida}'")
    except Exception as e:
        print(f"✗ Erro ao salvar relatório: {e}")


# ============================================
# MAIN - EXECUÇÃO COMPLETA
# ============================================

def main():
    print("=" * 60)
    print("IMPORTAÇÃO E TESTE DE DATASET")
    print("Varejo Online Musical")
    print("=" * 60)
    
    # 1. Conectar
    print("\n🔌 Conectando ao banco de dados...")
    conn = conectar_banco(DB_CONFIG)
    cursor = conn.cursor()
    
    # 2. Criar banco
    criar_banco(conn, cursor)
    usar_banco(conn, cursor)
    
    # 3. Criar tabela
    criar_tabela(conn, cursor)
    
    # 4. Ler CSV
    df = ler_csv(CSV_FILE)
    
    # 5. Importar
    importar_csv(conn, cursor, df)
    
    # 6. Validar
    valido = validar_dados(cursor)
    
    if not valido:
        print("\n⚠️  AVISO: Alguns testes falharam!")
        print("Verifique os dados do CSV")
    else:
        print("\n✅ Todos os testes de integridade passaram!")
    
    # 7. Relatórios
    gerar_relatorios(cursor)
    
    # 8. Ground Truth
    testar_ground_truth(cursor)
    
    # 9. Salvar relatório
    salvar_relatorio(cursor)
    
    # 10. Fechar conexão
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("  1. Verifique o relatório gerado")
    print("  2. Execute queries SQL em seu cliente")
    print("  3. Se precisar limpar, use: DROP DATABASE varejo_musical;")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        sys.exit(1)
