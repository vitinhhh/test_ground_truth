import importlib.util
from pathlib import Path


PASTA_SCRIPTS = Path(__file__).parent

ARQUIVO_LEXICAL = PASTA_SCRIPTS / "04_busca_lexical.py"
ARQUIVO_SEMANTICO = PASTA_SCRIPTS / "05_busca_semantica.py"


def carregar_modulo(caminho, nome):

    especificacao = importlib.util.spec_from_file_location(
        nome,
        caminho
    )

    modulo = importlib.util.module_from_spec(especificacao)

    especificacao.loader.exec_module(modulo)

    return modulo


lexical = carregar_modulo(
    ARQUIVO_LEXICAL,
    "busca_lexical"
)

semantico = carregar_modulo(
    ARQUIVO_SEMANTICO,
    "busca_semantica"
)


def normalizar_score(score, maior_score):

    if maior_score == 0:
        return 0

    return score / maior_score


def buscar_hibrida(query, limite=10):

    resultados_lexical = lexical.buscar_lexical(
        query,
        limite=limite
    )

    resultados_semanticos = semantico.buscar_semantica(
        query,
        limite=limite
    )

    produtos = {}

    for resultado in resultados_lexical:

        produto_id = resultado["produto_id"]

        produtos[produto_id] = {
            "produto_id": produto_id,
            "nome_produto": resultado["nome_produto"],
            "categoria": resultado["categoria"],
            "marca": resultado["marca"],
            "preco_unitario": resultado["preco_unitario"],
            "quantidade_estoque": resultado["quantidade_estoque"],
            "score_lexical": resultado["score"],
            "score_semantico": 0
        }

    for resultado in resultados_semanticos:

        produto_id = resultado["produto_id"]

        if produto_id not in produtos:

            produtos[produto_id] = {
                "produto_id": produto_id,
                "nome_produto": resultado["nome_produto"],
                "categoria": resultado["categoria"],
                "marca": resultado["marca"],
                "preco_unitario": resultado["preco_unitario"],
                "quantidade_estoque": resultado["quantidade_estoque"],
                "score_lexical": 0,
                "score_semantico": resultado["similaridade"]
            }

        else:

            produtos[produto_id]["score_semantico"] = (
                resultado["similaridade"]
            )

    produtos = list(produtos.values())

    maior_score_lexical = max(
        produto["score_lexical"]
        for produto in produtos
    )

    maior_score_semantico = max(
        produto["score_semantico"]
        for produto in produtos
    )

    for produto in produtos:

        score_lexical_normalizado = normalizar_score(
            produto["score_lexical"],
            maior_score_lexical
        )

        score_semantico_normalizado = normalizar_score(
            produto["score_semantico"],
            maior_score_semantico
        )

        produto["score_hibrido"] = (
            0.5 * score_lexical_normalizado
            + 0.5 * score_semantico_normalizado
        )

    produtos.sort(
        key=lambda produto: produto["score_hibrido"],
        reverse=True
    )

    return produtos[:limite]


if __name__ == "__main__":

    query = input("\nDigite sua busca: ").strip()

    print("\nTestando busca lexical...")

    resultado_lexical = lexical.buscar_lexical(
        query,
        limite=3
    )

    print(resultado_lexical)

    print("\nTestando busca semântica...")

    resultado_semantico = semantico.buscar_semantica(
        query,
        limite=3
    )

    print(resultado_semantico)

    resultados = buscar_hibrida(
        query,
        limite=10
    )

    print("\n========================================")
    print(" RESULTADOS DA BUSCA HÍBRIDA")
    print("========================================")

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
            f"   Score lexical: "
            f"{resultado['score_lexical']}"
        )

        print(
            f"   Score semântico: "
            f"{resultado['score_semantico']:.4f}"
        )

        print(
            f"   Score híbrido: "
            f"{resultado['score_hibrido']:.4f}"
        )

        print()