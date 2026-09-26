import csv
import os
import importlib.util
import math


# ============================================================
# CONFIGURAÇÃO
# ============================================================

CAMINHO_GT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Testes",
    "ground_truth.csv"
)

CAMINHO_LEXICAL = os.path.join(
    os.path.dirname(__file__),
    "04_busca_lexical.py"
)

CAMINHO_SEMANTICA = os.path.join(
    os.path.dirname(__file__),
    "05_busca_semantica.py"
)

CAMINHO_HIBRIDA = os.path.join(
    os.path.dirname(__file__),
    "06_busca_hibrida.py"
)

K = 5


# ============================================================
# CARREGAR MÓDULOS DE BUSCA
# ============================================================

def carregar_modulo(nome, caminho):

    especificacao = importlib.util.spec_from_file_location(
        nome,
        caminho
    )

    modulo = importlib.util.module_from_spec(
        especificacao
    )

    especificacao.loader.exec_module(modulo)

    return modulo


print("Carregando busca lexical...")

modulo_lexical = carregar_modulo(
    "busca_lexical",
    CAMINHO_LEXICAL
)

print("Busca lexical carregada.")


print("\nCarregando busca semântica...")

modulo_semantica = carregar_modulo(
    "busca_semantica",
    CAMINHO_SEMANTICA
)

print("Busca semântica carregada.")


print("\nCarregando busca híbrida...")

modulo_hibrida = carregar_modulo(
    "busca_hibrida",
    CAMINHO_HIBRIDA
)

print("Busca híbrida carregada.")


buscar_lexical = modulo_lexical.buscar_lexical
buscar_semantica = modulo_semantica.buscar_semantica
buscar_hibrida = modulo_hibrida.buscar_hibrida


# ============================================================
# CARREGAR GROUND TRUTH
# ============================================================

def carregar_ground_truth():

    with open(
        CAMINHO_GT,
        "r",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        registros = list(leitor)

    return registros


# ============================================================
# ORGANIZAR GROUND TRUTH
# ============================================================

def organizar_ground_truth(registros):

    ground_truth = {}

    for registro in registros:

        query = registro["query"]

        produto_id = int(
            registro["produto_id"]
        )

        relevancia = int(
            registro["relevancia"]
        )

        if query not in ground_truth:

            ground_truth[query] = {}

        ground_truth[query][produto_id] = relevancia

    return ground_truth


# ============================================================
# PRECISION@K
# ============================================================

def calcular_precision(resultados, relevancias, k):

    resultados_k = resultados[:k]

    if not resultados_k:

        return 0.0

    relevantes = 0

    for produto in resultados_k:

        produto_id = produto["produto_id"]

        if relevancias.get(produto_id, 0) > 0:

            relevantes += 1

    return relevantes / len(resultados_k)


# ============================================================
# RECALL@K
# ============================================================

def calcular_recall(resultados, relevancias, k):

    resultados_k = resultados[:k]

    relevantes_encontrados = 0

    for produto in resultados_k:

        produto_id = produto["produto_id"]

        if relevancias.get(produto_id, 0) > 0:

            relevantes_encontrados += 1

    total_relevantes = sum(
        1
        for relevancia in relevancias.values()
        if relevancia > 0
    )

    if total_relevantes == 0:

        return 0.0

    return relevantes_encontrados / total_relevantes


# ============================================================
# MRR
# ============================================================

def calcular_reciprocal_rank(resultados, relevancias):

    for posicao, produto in enumerate(
        resultados,
        start=1
    ):

        produto_id = produto["produto_id"]

        if relevancias.get(produto_id, 0) > 0:

            return 1 / posicao

    return 0.0


# ============================================================
# NDCG@K
# ============================================================

def calcular_ndcg(resultados, relevancias, k):

    resultados_k = resultados[:k]

    ganhos = []

    for produto in resultados_k:

        produto_id = produto["produto_id"]

        relevancia = relevancias.get(
            produto_id,
            0
        )

        ganho = (
            2 ** relevancia - 1
        )

        ganhos.append(ganho)

    dcg = 0.0

    for posicao, ganho in enumerate(
        ganhos,
        start=1
    ):

        dcg += ganho / math.log2(
            posicao + 1
        )

    relevancias_ideais = sorted(
        relevancias.values(),
        reverse=True
    )[:k]

    idcg = 0.0

    for posicao, relevancia in enumerate(
        relevancias_ideais,
        start=1
    ):

        ganho = (
            2 ** relevancia - 1
        )

        idcg += ganho / math.log2(
            posicao + 1
        )

    if idcg == 0:

        return 0.0

    return dcg / idcg


# ============================================================
# AVALIAR UM MÉTODO
# ============================================================

def avaliar_metodo(
    nome_metodo,
    funcao_busca,
    ground_truth
):

    print("\n" + "=" * 60)
    print(f" AVALIANDO: {nome_metodo}")
    print("=" * 60)

    resultados_metricas = []

    for query, relevancias in ground_truth.items():

        print(
            f"\nQuery: {query}"
        )

        resultados = funcao_busca(
            query,
            limite=10
        )

        mrr = calcular_reciprocal_rank(
            resultados,
            relevancias
        )

        ndcg = calcular_ndcg(
            resultados,
            relevancias,
            K
        )

        precision = calcular_precision(
            resultados,
            relevancias,
            K
        )

        recall = calcular_recall(
            resultados,
            relevancias,
            K
        )

        resultados_metricas.append({
            "query": query,
            "mrr": mrr,
            "ndcg": ndcg,
            "precision": precision,
            "recall": recall
        })

        print(
            f"  MRR:        {mrr:.4f}"
        )

        print(
            f"  NDCG@{K}:    {ndcg:.4f}"
        )

        print(
            f"  Precision@{K}: {precision:.4f}"
        )

        print(
            f"  Recall@{K}:    {recall:.4f}"
        )

    return resultados_metricas


# ============================================================
# CALCULAR MÉDIA
# ============================================================

def calcular_media(resultados):

    quantidade = len(resultados)

    if quantidade == 0:

        return {
            "mrr": 0.0,
            "ndcg": 0.0,
            "precision": 0.0,
            "recall": 0.0
        }

    return {
        "mrr": sum(
            resultado["mrr"]
            for resultado in resultados
        ) / quantidade,

        "ndcg": sum(
            resultado["ndcg"]
            for resultado in resultados
        ) / quantidade,

        "precision": sum(
            resultado["precision"]
            for resultado in resultados
        ) / quantidade,

        "recall": sum(
            resultado["recall"]
            for resultado in resultados
        ) / quantidade
    }


# ============================================================
# COMPARAÇÃO POR QUERY
# ============================================================

def mostrar_comparacao(
    metricas_lexical,
    metricas_semantica,
    metricas_hibrida
):

    print("\n" + "=" * 100)
    print(" COMPARAÇÃO POR QUERY")
    print("=" * 100)

    for lexical, semantica, hibrida in zip(
        metricas_lexical,
        metricas_semantica,
        metricas_hibrida
    ):

        print(
            f"\nQuery: {lexical['query']}"
        )

        print(
            f"  {'Método':<12}"
            f"{'MRR':>10}"
            f"{'NDCG@5':>12}"
            f"{'Precision@5':>15}"
            f"{'Recall@5':>12}"
        )

        print(
            f"  {'Lexical':<12}"
            f"{lexical['mrr']:>10.4f}"
            f"{lexical['ndcg']:>12.4f}"
            f"{lexical['precision']:>15.4f}"
            f"{lexical['recall']:>12.4f}"
        )

        print(
            f"  {'Semântica':<12}"
            f"{semantica['mrr']:>10.4f}"
            f"{semantica['ndcg']:>12.4f}"
            f"{semantica['precision']:>15.4f}"
            f"{semantica['recall']:>12.4f}"
        )

        print(
            f"  {'Híbrida':<12}"
            f"{hibrida['mrr']:>10.4f}"
            f"{hibrida['ndcg']:>12.4f}"
            f"{hibrida['precision']:>15.4f}"
            f"{hibrida['recall']:>12.4f}"
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print(" AVALIAÇÃO DOS MÉTODOS DE BUSCA")
    print("=" * 60)

    registros = carregar_ground_truth()

    ground_truth = organizar_ground_truth(
        registros
    )

    print(
        f"\nGround Truth carregado: "
        f"{len(ground_truth)} queries"
    )

    # --------------------------------------------------------
    # AVALIAR LEXICAL
    # --------------------------------------------------------

    metricas_lexical = avaliar_metodo(
        "LEXICAL",
        buscar_lexical,
        ground_truth
    )

    # --------------------------------------------------------
    # AVALIAR SEMÂNTICA
    # --------------------------------------------------------

    metricas_semantica = avaliar_metodo(
        "SEMÂNTICA",
        buscar_semantica,
        ground_truth
    )

    # --------------------------------------------------------
    # AVALIAR HÍBRIDA
    # --------------------------------------------------------

    metricas_hibrida = avaliar_metodo(
        "HÍBRIDA",
        buscar_hibrida,
        ground_truth
    )

    # --------------------------------------------------------
    # CALCULAR MÉDIAS
    # --------------------------------------------------------

    media_lexical = calcular_media(
        metricas_lexical
    )

    media_semantica = calcular_media(
        metricas_semantica
    )

    media_hibrida = calcular_media(
        metricas_hibrida
    )

    # --------------------------------------------------------
    # RESULTADO FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print(" RESULTADO FINAL")
    print("=" * 60)

    print("\nLEXICAL")

    print(
        f"MRR:          {media_lexical['mrr']:.4f}"
    )

    print(
        f"NDCG@{K}:      {media_lexical['ndcg']:.4f}"
    )

    print(
        f"Precision@{K}: {media_lexical['precision']:.4f}"
    )

    print(
        f"Recall@{K}:    {media_lexical['recall']:.4f}"
    )

    print("\nSEMÂNTICA")

    print(
        f"MRR:          {media_semantica['mrr']:.4f}"
    )

    print(
        f"NDCG@{K}:      {media_semantica['ndcg']:.4f}"
    )

    print(
        f"Precision@{K}: {media_semantica['precision']:.4f}"
    )

    print(
        f"Recall@{K}:    {media_semantica['recall']:.4f}"
    )

    print("\nHÍBRIDA")

    print(
        f"MRR:          {media_hibrida['mrr']:.4f}"
    )

    print(
        f"NDCG@{K}:      {media_hibrida['ndcg']:.4f}"
    )

    print(
        f"Precision@{K}: {media_hibrida['precision']:.4f}"
    )

    print(
        f"Recall@{K}:    {media_hibrida['recall']:.4f}"
    )

    # --------------------------------------------------------
    # COMPARAÇÃO POR QUERY
    # --------------------------------------------------------

    mostrar_comparacao(
        metricas_lexical,
        metricas_semantica,
        metricas_hibrida
    )

    print("\n" + "=" * 60)
    print(" AVALIAÇÃO CONCLUÍDA")
    print("=" * 60)