from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306
}

DATABASE = "varejo_musical"


print("========================================")
print(" BUSCA SEMÂNTICA")
print("========================================")


print("\nCarregando modelo...")

modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Modelo carregado com sucesso!")


def conectar_banco():

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
        database=DATABASE
    )


def carregar_produtos():

    print("\nConectando ao banco...")

    conexao = conectar_banco()

    print("Banco conectado com sucesso!")

    cursor = conexao.cursor(dictionary=True)

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

    print(
        f"Produtos ativos encontrados: "
        f"{len(produtos)}"
    )

    return produtos


def criar_texto_produto(produto):

    texto = f"""
    {produto['nome_produto']}.
    Categoria: {produto['categoria']}.
    Marca: {produto['marca']}.
    Descrição: {produto['descricao_longa']}.
    Tags: {produto['tags']}.
    Especificações: {produto['especificacoes']}.
    """

    return texto.strip()


produtos = carregar_produtos()


print("\n========================================")
print(" GERANDO EMBEDDINGS DOS PRODUTOS")
print("========================================")


textos_produtos = [
    criar_texto_produto(produto)
    for produto in produtos
]


embeddings_produtos = modelo.encode(
    textos_produtos,
    show_progress_bar=True
)


print("\nEmbeddings gerados com sucesso!")

print(
    f"Quantidade de produtos: "
    f"{len(embeddings_produtos)}"
)

print(
    f"Tamanho de cada embedding: "
    f"{len(embeddings_produtos[0])}"
)


def buscar_semantica(query, limite=10):

    embedding_query = modelo.encode(
        [query]
    )

    similaridades = cosine_similarity(
        embedding_query,
        embeddings_produtos
    )[0]

    resultados = []

    for produto, similaridade in zip(
        produtos,
        similaridades
    ):

        resultados.append({
            "produto_id": produto["produto_id"],
            "nome_produto": produto["nome_produto"],
            "categoria": produto["categoria"],
            "marca": produto["marca"],
            "preco_unitario": produto["preco_unitario"],
            "quantidade_estoque": produto["quantidade_estoque"],
            "similaridade": float(similaridade)
        })

    resultados.sort(
        key=lambda resultado: resultado["similaridade"],
        reverse=True
    )

    return resultados[:limite]


def mostrar_resultados(query, resultados):

    print("\n========================================")
    print(" RESULTADOS DA BUSCA SEMÂNTICA")
    print("========================================")

    print(
        f"\nConsulta: {query}\n"
    )

    if not resultados:

        print("Nenhum produto encontrado.")

        return

    for posicao, resultado in enumerate(
        resultados,
        start=1
    ):

        print(
            f"{posicao}. "
            f"{resultado['nome_produto']} "
            f"(ID: {resultado['produto_id']})"
        )

        print(
            f"   Categoria: "
            f"{resultado['categoria']}"
        )

        print(
            f"   Marca: "
            f"{resultado['marca']}"
        )

        print(
            f"   Preço: "
            f"R$ {resultado['preco_unitario']}"
        )

        print(
            f"   Estoque: "
            f"{resultado['quantidade_estoque']}"
        )

        print(
            f"   Similaridade: "
            f"{resultado['similaridade']:.4f}"
        )

        print()


if __name__ == "__main__":

    while True:

        query = input(
            "\nDigite sua busca semântica: "
        ).strip()

        if not query:

            print("\nConsulta vazia.")

            continue

        resultados = buscar_semantica(query)

        mostrar_resultados(
            query,
            resultados
        )

        continuar = input(
            "Deseja fazer outra busca? (s/n): "
        ).strip().lower()

        if continuar != "s":

            print(
                "\nEncerrando busca semântica..."
            )

            break