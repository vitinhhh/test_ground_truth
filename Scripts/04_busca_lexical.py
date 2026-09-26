import re
import unicodedata
import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306
}

DATABASE = "varejo_musical"


STOPWORDS = {
    "a", "o", "as", "os",
    "um", "uma",
    "de", "do", "da", "dos", "das",
    "para", "com", "e", "em"
}


def conectar_banco():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
        database=DATABASE
    )


def normalizar_texto(texto):

    if not texto:
        return ""

    texto = str(texto).lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    texto = re.sub(
        r"[^a-z0-9\s]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def extrair_termos(query):

    query_normalizada = normalizar_texto(query)

    termos = query_normalizada.split()

    termos = [
        termo
        for termo in termos
        if termo not in STOPWORDS
    ]

    return termos


def calcular_score(produto, termos, query):

    campos = {
        "nome_produto": (
            produto["nome_produto"],
            5
        ),

        "categoria": (
            produto["categoria"],
            3
        ),

        "tags": (
            produto["tags"],
            2
        ),

        "descricao_longa": (
            produto["descricao_longa"],
            1
        ),

        "especificacoes": (
            produto["especificacoes"],
            1
        )
    }

    score = 0

    for termo in termos:

        for valor, peso in campos.values():

            if not valor:
                continue

            texto = normalizar_texto(valor)

            if termo in texto:
                score += peso

    query_normalizada = normalizar_texto(query)

    nome_normalizado = normalizar_texto(
        produto["nome_produto"]
    )

    if query_normalizada in nome_normalizado:
        score += 10

    return score


def buscar_lexical(query, limite=10):

    conexao = conectar_banco()

    cursor = conexao.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            produto_id,
            nome_produto,
            categoria,
            marca,
            descricao_longa,
            preco_unitario,
            quantidade_estoque,
            tags,
            especificacoes,
            status
        FROM produtos
        WHERE status = 'ativo'
    """)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    termos = extrair_termos(query)

    resultados = []

    for produto in produtos:

        score = calcular_score(
            produto,
            termos,
            query
        )

        if score > 0:

            resultados.append({
                "produto_id": produto["produto_id"],
                "nome_produto": produto["nome_produto"],
                "categoria": produto["categoria"],
                "marca": produto["marca"],
                "preco_unitario": produto["preco_unitario"],
                "quantidade_estoque": produto["quantidade_estoque"],
                "score": score
            })

    resultados.sort(
        key=lambda produto: (
            -produto["score"],
            produto["produto_id"]
        )
    )

    return resultados[:limite]


def mostrar_resultados(query, resultados):

    print("\n========================================")
    print(" BUSCA LEXICAL")
    print("========================================")

    print(
        f"\nConsulta: {query}"
    )

    if not resultados:

        print(
            "\nNenhum produto encontrado."
        )

        return

    print(
        f"\nResultados encontrados: "
        f"{len(resultados)}\n"
    )

    for posicao, produto in enumerate(
        resultados,
        start=1
    ):

        print(
            f"{posicao}. "
            f"{produto['nome_produto']} "
            f"(ID: {produto['produto_id']})"
        )

        print(
            f"   Categoria: "
            f"{produto['categoria']}"
        )

        print(
            f"   Marca: "
            f"{produto['marca']}"
        )

        print(
            f"   Preço: "
            f"R$ {produto['preco_unitario']}"
        )

        print(
            f"   Estoque: "
            f"{produto['quantidade_estoque']}"
        )

        print(
            f"   Score lexical: "
            f"{produto['score']}"
        )

        print()


if __name__ == "__main__":

    print("========================================")
    print(" SISTEMA DE BUSCA LEXICAL")
    print("========================================")

    query = input(
        "\nDigite sua busca: "
    ).strip()

    if not query:

        print(
            "\nConsulta vazia."
        )

    else:

        try:

            resultados = buscar_lexical(
                query
            )

            mostrar_resultados(
                query,
                resultados
            )

        except Exception as erro:

            print(
                "\n========================================"
            )

            print(
                " ERRO DURANTE A BUSCA"
            )

            print(
                "========================================"
            )

            print(
                f"\n{type(erro).__name__}: {erro}"
            )