import pandas as pd
import mysql.connector


# ============================================================
# CONFIGURAÇÃO
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306
}

DATABASE = "varejo_musical"

CSV_PATH = "Scripts/dataset_robusto_500produtos.csv"


# ============================================================
# CONEXÃO COM O MYSQL
# ============================================================

def conectar_mysql():
    """
    Cria uma conexão com o servidor MySQL.
    """

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )


# ============================================================
# CRIAÇÃO DO BANCO
# ============================================================

def criar_banco():
    """
    Cria o banco de dados caso ele ainda não exista.
    """

    conexao = conectar_mysql()
    cursor = conexao.cursor()

    print("Verificando banco de dados...")

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DATABASE}"
    )

    conexao.commit()

    print(f"Banco '{DATABASE}' pronto.")

    cursor.close()
    conexao.close()


# ============================================================
# CRIAÇÃO DA TABELA
# ============================================================

def criar_tabela():
    """
    Cria a tabela produtos de acordo com o CSV atual.
    """

    conexao = conectar_mysql()
    cursor = conexao.cursor()

    cursor.execute(f"USE {DATABASE}")

    print("Recriando tabela 'produtos'...")

    # Como estamos reconstruindo o banco do zero,
    # removemos a tabela anterior.
    cursor.execute("DROP TABLE IF EXISTS produtos")

    cursor.execute("""
        CREATE TABLE produtos (

            produto_id INT PRIMARY KEY,

            nome_produto VARCHAR(255) NOT NULL,

            categoria VARCHAR(100) NOT NULL,

            marca VARCHAR(100) NOT NULL,

            descricao_longa TEXT,

            preco_unitario DECIMAL(10, 2) NOT NULL,

            quantidade_estoque INT NOT NULL,

            rating DECIMAL(3, 2),

            num_reviews INT,

            reviews TEXT,

            tags TEXT,

            especificacoes TEXT,

            fornecedor VARCHAR(100),

            sku VARCHAR(50) UNIQUE,

            status VARCHAR(20) NOT NULL,

            data_adicao DATE

        )
    """)

    conexao.commit()

    print("Tabela 'produtos' criada.")

    cursor.close()
    conexao.close()


# ============================================================
# VALIDAÇÃO DO CSV
# ============================================================

def validar_csv(df):
    """
    Verifica se o CSV possui todas as colunas esperadas.
    """

    colunas_esperadas = [
        "produto_id",
        "nome_produto",
        "categoria",
        "marca",
        "descricao_longa",
        "preco_unitario",
        "quantidade_estoque",
        "rating",
        "num_reviews",
        "reviews",
        "tags",
        "especificacoes",
        "fornecedor",
        "sku",
        "status",
        "data_adicao"
    ]

    colunas_faltantes = [
        coluna
        for coluna in colunas_esperadas
        if coluna not in df.columns
    ]

    if colunas_faltantes:

        print("\nERRO: o CSV não possui as seguintes colunas:")

        for coluna in colunas_faltantes:
            print(f" - {coluna}")

        raise ValueError(
            "O CSV não possui todas as colunas esperadas."
        )

    print("Estrutura do CSV validada.")
    print(f"Total de colunas: {len(df.columns)}")


# ============================================================
# IMPORTAÇÃO DO CSV
# ============================================================

def importar_csv():
    """
    Lê o CSV e insere os produtos no MySQL.
    """

    print("\nLendo dataset...")

    df = pd.read_csv(CSV_PATH)

    print(f"Produtos encontrados: {len(df)}")

    validar_csv(df)

    conexao = conectar_mysql()
    cursor = conexao.cursor()

    cursor.execute(f"USE {DATABASE}")

    sql = """
        INSERT INTO produtos (

            produto_id,
            nome_produto,
            categoria,
            marca,
            descricao_longa,
            preco_unitario,
            quantidade_estoque,
            rating,
            num_reviews,
            reviews,
            tags,
            especificacoes,
            fornecedor,
            sku,
            status,
            data_adicao

        )

        VALUES (

            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s

        )
    """

    print("\nIniciando importação...")

    contador = 0

    for _, produto in df.iterrows():

        valores = (

            int(produto["produto_id"]),

            produto["nome_produto"],

            produto["categoria"],

            produto["marca"],

            produto["descricao_longa"],

            float(produto["preco_unitario"]),

            int(produto["quantidade_estoque"]),

            float(produto["rating"]),

            int(produto["num_reviews"]),

            produto["reviews"],

            produto["tags"],

            produto["especificacoes"],

            produto["fornecedor"],

            produto["sku"],

            produto["status"],

            produto["data_adicao"]

        )

        cursor.execute(sql, valores)

        contador += 1

        # Mostra progresso a cada 100 produtos
        if contador % 100 == 0:
            print(f"  {contador} produtos importados...")

    conexao.commit()

    print(f"\nImportação concluída!")
    print(f"Total importado: {contador} produtos.")

    cursor.close()
    conexao.close()


# ============================================================
# TESTE DO BANCO
# ============================================================

def testar_banco():
    """
    Faz algumas verificações para garantir que a importação
    ocorreu corretamente.
    """

    conexao = conectar_mysql()
    cursor = conexao.cursor()

    cursor.execute(f"USE {DATABASE}")

    # --------------------------------------------------------
    # Quantidade total
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM produtos
    """)

    quantidade = cursor.fetchone()[0]

    print("\n========================================")
    print("TESTE DO BANCO")
    print("========================================")

    print(f"\nTotal de produtos no banco: {quantidade}")

    # --------------------------------------------------------
    # Primeiros produtos
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            produto_id,
            nome_produto,
            categoria,
            preco_unitario,
            quantidade_estoque,
            status
        FROM produtos
        ORDER BY produto_id
        LIMIT 5
    """)

    produtos = cursor.fetchall()

    print("\nPrimeiros 5 produtos:")

    for produto in produtos:

        print(
            f"ID: {produto[0]} | "
            f"{produto[1]} | "
            f"Categoria: {produto[2]} | "
            f"Preço: R$ {produto[3]} | "
            f"Estoque: {produto[4]} | "
            f"Status: {produto[5]}"
        )

    # --------------------------------------------------------
    # Categorias
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            categoria,
            COUNT(*)
        FROM produtos
        GROUP BY categoria
        ORDER BY categoria
    """)

    categorias = cursor.fetchall()

    print("\nProdutos por categoria:")

    for categoria, quantidade_categoria in categorias:

        print(
            f" - {categoria}: "
            f"{quantidade_categoria}"
        )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            status,
            COUNT(*)
        FROM produtos
        GROUP BY status
        ORDER BY status
    """)

    status = cursor.fetchall()

    print("\nProdutos por status:")

    for status_produto, quantidade_status in status:

        print(
            f" - {status_produto}: "
            f"{quantidade_status}"
        )

    cursor.close()
    conexao.close()


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print(" IMPORTAÇÃO DO DATASET")
    print("========================================")

    try:

        # 1. Criar banco
        criar_banco()

        # 2. Criar tabela
        criar_tabela()

        # 3. Importar CSV
        importar_csv()

        # 4. Testar banco
        testar_banco()

        print("\n========================================")
        print(" IMPORTAÇÃO FINALIZADA COM SUCESSO")
        print("========================================")

    except Exception as erro:

        print("\n========================================")
        print(" ERRO DURANTE A IMPORTAÇÃO")
        print("========================================")

        print(f"\n{type(erro).__name__}: {erro}")

        print("\nA importação foi interrompida.")