import csv
import os
import re
import requests
import mysql.connector


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306,
    "database": "varejo_musical"
}

ARQUIVO_GROUND_TRUTH = "Testes/ground_truth.csv"
ARQUIVO_SAIDA = "Testes/ground_truth_validado_llm.csv"


def conectar_banco():

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"]
    )


def buscar_produto(produto_id):

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            produto_id,
            nome_produto,
            categoria,
            descricao_longa,
            tags,
            especificacoes
        FROM produtos
        WHERE produto_id = %s
    """, (produto_id,))

    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    return produto


def montar_produto(produto):

    return f"""
Nome: {produto["nome_produto"]}
Categoria: {produto["categoria"]}
Descrição: {produto["descricao_longa"]}
Tags: {produto["tags"]}
Especificações: {produto["especificacoes"]}
"""


def avaliar_com_llm(query, produto, relevancia_manual):

    prompt = f"""
Você é um revisor independente de um Ground Truth de busca de produtos.

CONSULTA:
{query}

PRODUTO:
{produto}

CLASSIFICAÇÃO MANUAL:
{relevancia_manual}

ESCALA DA CLASSIFICAÇÃO MANUAL:
5 = atende diretamente à consulta
4 = atende muito bem, com pequena diferença
3 = relacionado e parcialmente adequado, mas possui diferença relevante
2 = relação indireta
1 = relação muito fraca
0 = não atende à consulta

TAREFA:
Analise se a classificação manual é coerente com a consulta e o produto.

Não avalie apenas se o produto pertence ao mesmo universo ou categoria.
Considere se ele realmente atende à intenção específica da consulta.

IMPORTANTE:
Você está revisando a classificação manual.
Não deve alterar a classificação.
Não deve criar uma nova nota.

Responda exatamente neste formato:

AVALIACAO: CONCORDO

JUSTIFICATIVA: uma frase curta explicando o motivo.

OU:

AVALIACAO: DISCORDO

JUSTIFICATIVA: uma frase curta explicando o motivo.

Não invente informações que não estejam na consulta ou no produto.
"""

    dados = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 100
        }
    }

    resposta = requests.post(
        OLLAMA_URL,
        json=dados,
        timeout=120
    )

    resposta.raise_for_status()

    texto = resposta.json()["response"].strip()

    avaliacao = re.search(
        r"AVALIACAO:\s*(CONCORDO|DISCORDO)",
        texto,
        re.IGNORECASE
    )

    justificativa = re.search(
        r"JUSTIFICATIVA:\s*(.*)",
        texto,
        re.IGNORECASE | re.DOTALL
    )

    if avaliacao:
        avaliacao = avaliacao.group(1).upper()
    else:
        avaliacao = "ERRO"

    if justificativa:
        justificativa = justificativa.group(1).strip()
    else:
        justificativa = texto

    return avaliacao, justificativa


def carregar_resultados_existentes():

    resultados = {}

    if not os.path.exists(ARQUIVO_SAIDA):
        return resultados

    with open(
        ARQUIVO_SAIDA,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:

            chave = (
                linha["query"],
                linha["produto_id"]
            )

            resultados[chave] = linha

    return resultados


def salvar_resultado(linha):

    arquivo_existe = os.path.exists(ARQUIVO_SAIDA)

    with open(
        ARQUIVO_SAIDA,
        "a",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        campos = [
            "query",
            "produto_id",
            "relevancia_manual",
            "avaliacao_llm",
            "justificativa_llm"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        if not arquivo_existe:
            escritor.writeheader()

        escritor.writerow(linha)


def main():

    resultados_existentes = carregar_resultados_existentes()

    with open(
        ARQUIVO_GROUND_TRUTH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        registros = list(leitor)

    total = len(registros)

    print("=" * 70)
    print("VALIDAÇÃO DO GROUND TRUTH COM LLM")
    print("=" * 70) 
    print(f"Total de registros: {total}")
    print(f"Já processados: {len(resultados_existentes)}")
    print()

    for indice, registro in enumerate(registros, start=1):

        query = registro["query"]
        produto_id = registro["produto_id"]
        relevancia_manual = registro["relevancia"]

        chave = (query, produto_id)

        if chave in resultados_existentes:

            print(
                f"[{indice}/{total}] "
                f"Já processado: {query} - produto {produto_id}"
            )

            continue

        print("=" * 70)
        print(
            f"[{indice}/{total}] "
            f"{query} | produto {produto_id}"
        )

        produto = buscar_produto(produto_id)

        if not produto:

            print("Produto não encontrado no banco.")
            continue

        produto_texto = montar_produto(produto)

        try:

            avaliacao, justificativa = avaliar_com_llm(
                query,
                produto_texto,
                relevancia_manual
            )

        except Exception as erro:

            print(f"Erro ao consultar o LLM: {erro}")
            continue

        linha = {
            "query": query,
            "produto_id": produto_id,
            "relevancia_manual": relevancia_manual,
            "avaliacao_llm": avaliacao,
            "justificativa_llm": justificativa
        }

        salvar_resultado(linha)

        print(f"GT manual: {relevancia_manual}")
        print(f"LLM: {avaliacao}")
        print(f"Justificativa: {justificativa}")

    print()
    print("=" * 70)
    print("VALIDAÇÃO FINALIZADA")
    print("=" * 70)
    print(f"Arquivo: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()