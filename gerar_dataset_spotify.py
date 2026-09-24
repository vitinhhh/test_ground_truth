
"""
Requisitos:
    pip install spotipy faker pandas
    
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

# ============================================
# CONFIGURAÇÃO SPOTIFY API
# ============================================
# Você precisa de:
# 1. Criar app em https://developer.spotify.com/dashboard
# 2. Gerar Client ID e Client Secret
# 3. Copiar aqui:

CLIENT_ID = "SUA_CLIENT_ID_AQUI"
CLIENT_SECRET = "SUA_CLIENT_SECRET_AQUI"

# ============================================
# DADOS DE CATÁLOGO MUSICAL (fallback se API falhar)
# ============================================
INSTRUMENTOS = [
    {"nome": "Guitarra Acústica 41 Polegadas", "categoria": "Instrumentos", "marca": "Tagima", "preco_base": 150},
    {"nome": "Teclado Sintetizador 61 Teclas", "categoria": "Instrumentos", "marca": "Yamaha", "preco_base": 1500},
    {"nome": "Bateria Acústica 5 Peças", "categoria": "Instrumentos", "marca": "Pearl", "preco_base": 2000},
    {"nome": "Violão Clássico Nylon", "categoria": "Instrumentos", "marca": "Fender", "preco_base": 200},
    {"nome": "Saxofone Alto Eb Dourado", "categoria": "Instrumentos", "marca": "Selmer", "preco_base": 3500},
    {"nome": "Trompete Bb Latão", "categoria": "Instrumentos", "marca": "Yamaha", "preco_base": 1300},
    {"nome": "Clarinete Bb Madeira", "categoria": "Instrumentos", "marca": "Yamaha", "preco_base": 1200},
    {"nome": "Baixo Elétrico 4 Cordas", "categoria": "Instrumentos", "marca": "Ibanez", "preco_base": 650},
    {"nome": "Accordion Diatônico 120 Baixos", "categoria": "Instrumentos", "marca": "Hohner", "preco_base": 2500},
    {"nome": "Viola de Arco Profissional", "categoria": "Instrumentos", "marca": "Cremona", "preco_base": 2200},
]

ACESSORIOS = [
    {"nome": "Baqueta Nylon Colorida (Par)", "categoria": "Acessórios", "marca": "Vic Firth", "preco_base": 20},
    {"nome": "Capa Protetora para Violão", "categoria": "Acessórios", "marca": "Genérica", "preco_base": 35},
    {"nome": "Cabo XLR Balanceado 5M", "categoria": "Acessórios", "marca": "Behringer", "preco_base": 25},
    {"nome": "Stand para Guitarra Ajustável", "categoria": "Acessórios", "marca": "K&M", "preco_base": 70},
    {"nome": "Correia de Couro para Guitarra", "categoria": "Acessórios", "marca": "Leather Music", "preco_base": 55},
    {"nome": "Afinador Cromático Portátil", "categoria": "Acessórios", "marca": "Snark", "preco_base": 40},
    {"nome": "Capotrasto Clássico Premium", "categoria": "Acessórios", "marca": "Shubb", "preco_base": 75},
    {"nome": "Plectro de Aço Inoxidável", "categoria": "Acessórios", "marca": "Ernie Ball", "preco_base": 12},
    {"nome": "Corda de Aço para Violão", "categoria": "Acessórios", "marca": "D'Addario", "preco_base": 35},
    {"nome": "Humidificador para Violão", "categoria": "Acessórios", "marca": "Hohner", "preco_base": 65},
]

EQUIPAMENTOS = [
    {"nome": "Microfone Condensador USB", "categoria": "Áudio", "marca": "Audio-Technica", "preco_base": 120},
    {"nome": "Amplificador de Guitarra 50W", "categoria": "Equipamentos", "marca": "Marshall", "preco_base": 450},
    {"nome": "Pedal Distorção Analógico", "categoria": "Equipamentos", "marca": "Boss", "preco_base": 350},
    {"nome": "Interface de Áudio 2x2", "categoria": "Equipamentos", "marca": "Focusrite", "preco_base": 450},
    {"nome": "Alto-Falante Monitor 8 Polegadas", "categoria": "Equipamentos", "marca": "KRK", "preco_base": 650},
    {"nome": "Pad MIDI 16 Pads Controlador", "categoria": "Equipamentos", "marca": "Native Instruments", "preco_base": 900},
    {"nome": "Compressor de Áudio 2 Canais", "categoria": "Equipamentos", "marca": "dbx", "preco_base": 300},
    {"nome": "Gravador Digital 2 Canais", "categoria": "Equipamentos", "marca": "Zoom", "preco_base": 450},
    {"nome": "Processador de Efeitos Multifuncional", "categoria": "Equipamentos", "marca": "Line 6", "preco_base": 900},
    {"nome": "Fone Over-Ear Bluetooth", "categoria": "Áudio", "marca": "Sony", "preco_base": 250},
]

FORNECEDORES = [
    "Distribuidora Musical BR",
    "Tech Store Audio",
    "Eletrônicos Premium",
    "Music Supply",
    "ProMusic Store",
    "Guitar Center BR",
    "Proteção Music",
    "Tech Musical",
    "Conecta Audio",
    "Drums World",
]

# ============================================
# FUNÇÕES
# ============================================

def conectar_spotify():
    """Conecta na API do Spotify"""
    try:
        auth = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        sp = spotipy.Spotify(auth_manager=auth)
        print("✓ Conectado ao Spotify com sucesso!")
        return sp
    except Exception as e:
        print(f"✗ Erro ao conectar Spotify: {e}")
        print("→ Usando dados local como fallback...")
        return None


def buscar_artistas_spotify(sp, termo="music", limite=20):
    """Busca artistas no Spotify"""
    try:
        results = sp.search(q=termo, type='artist', limit=limite)
        artistas = []
        for item in results['artists']['items']:
            artistas.append({
                "nome": item['name'],
                "genres": item.get('genres', ['outro']),
                "popularidade": item.get('popularity', 50)
            })
        return artistas
    except Exception as e:
        print(f"✗ Erro ao buscar artistas: {e}")
        return []


def gerar_dataset(num_produtos=40, usar_spotify=True):
    """Gera dataset completo de varejo musical"""
    
    print(f"\n📊 Gerando dataset com {num_produtos} produtos...\n")
    
    sp = None
    artistas_reais = []
    
    if usar_spotify and CLIENT_ID != "SUA_CLIENT_ID_AQUI":
        sp = conectar_spotify()
        if sp:
            artistas_reais = buscar_artistas_spotify(sp, "music", 30)
            print(f"✓ {len(artistas_reais)} artistas carregados do Spotify\n")
    
    # Combinar dados
    todos_produtos = INSTRUMENTOS + ACESSORIOS + EQUIPAMENTOS
    random.shuffle(todos_produtos)
    
    fake = Faker('pt_BR')
    dataset = []
    
    # Extrair nomes de artistas do Spotify ou usar padrão
    nomes_artistas = [a["nome"] for a in artistas_reais] if artistas_reais else [
        "Fender", "Yamaha", "Marshall", "Boss", "Audio-Technica", "Sony",
        "Vic Firth", "Behringer", "KRK", "Zoom", "Native Instruments"
    ]
    
    for i in range(num_produtos):
        produto_base = todos_produtos[i % len(todos_produtos)]
        
        # Gerar variações do produto
        preco = produto_base["preco_base"] + random.uniform(-50, 150)
        preco = round(preco, 2)
        
        estoque = random.randint(1, 100)
        
        # Gerar data aleatória nos últimos 7 dias
        data_update = datetime.now() - timedelta(days=random.randint(0, 7))
        data_str = data_update.strftime("%Y-%m-%d")
        
        # Gerar SKU único
        sku = f"{produto_base['marca'][:3].upper()}-{produto_base['categoria'][:4].upper()}-{i+1:03d}"
        
        produto = {
            "produto_id": i + 1,
            "nome_produto": produto_base["nome"],
            "categoria": produto_base["categoria"],
            "artista_marca": produto_base["marca"],
            "preco_unitario": preco,
            "quantidade_estoque": estoque,
            "data_atualizacao": data_str,
            "fornecedor": random.choice(FORNECEDORES),
            "sku": sku,
            "status": "ativo" if estoque > 0 else "inativo"
        }
        
        dataset.append(produto)
    
    # Converter para DataFrame
    df = pd.DataFrame(dataset)
    
    return df


def salvar_csv(df, nome_arquivo="dataset_varejo_musical.csv"):
    """Salva dataset em CSV"""
    df.to_csv(nome_arquivo, index=False)
    print(f"✓ Arquivo '{nome_arquivo}' criado com sucesso!")
    print(f"  Tamanho: {len(df)} linhas, {len(df.columns)} colunas")


def salvar_ground_truth(df, nome_arquivo="ground_truth_exemplo.csv"):
    """Salva exemplo de Ground Truth para testes"""
    # Selecionar alguns produtos para ground truth
    ground_truth = df.sample(n=min(10, len(df)), random_state=42)[
        ["produto_id", "nome_produto", "categoria", "preco_unitario", "quantidade_estoque"]
    ].copy()
    
    ground_truth["categoria_esperada"] = ground_truth["categoria"]
    ground_truth["preco_esperado"] = ground_truth["preco_unitario"]
    ground_truth["estoque_esperado"] = ground_truth["quantidade_estoque"]
    
    ground_truth.to_csv(nome_arquivo, index=False)
    print(f"✓ Arquivo '{nome_arquivo}' criado com {len(ground_truth)} casos de teste!")


# ============================================
# EXEMPLO DE QUERIES (SQL)
# ============================================

EXEMPLO_QUERIES = """
-- EXEMPLOS DE QUERIES PARA O DATASET

-- 1. Produtos com estoque baixo (< 5 unidades)
SELECT produto_id, nome_produto, quantidade_estoque 
FROM produtos 
WHERE quantidade_estoque < 5 
ORDER BY quantidade_estoque ASC;

-- 2. Faturamento potencial por categoria
SELECT categoria, 
       COUNT(*) AS total_produtos,
       SUM(quantidade_estoque * preco_unitario) AS faturamento_potencial,
       AVG(preco_unitario) AS preco_medio
FROM produtos 
WHERE status = 'ativo'
GROUP BY categoria 
ORDER BY faturamento_potencial DESC;

-- 3. Produtos com maior valor em estoque
SELECT produto_id, nome_produto, artista_marca,
       quantidade_estoque, preco_unitario,
       (quantidade_estoque * preco_unitario) AS valor_total_estoque
FROM produtos 
WHERE status = 'ativo'
ORDER BY valor_total_estoque DESC
LIMIT 10;

-- 4. Produtos por fornecedor
SELECT fornecedor, COUNT(*) AS total_produtos
FROM produtos 
GROUP BY fornecedor
ORDER BY total_produtos DESC;

-- 5. Atualização de preços (últimos 3 dias)
SELECT produto_id, nome_produto, data_atualizacao
FROM produtos 
WHERE DATE(data_atualizacao) >= DATE_SUB(CURDATE(), INTERVAL 3 DAY)
ORDER BY data_atualizacao DESC;
"""


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("GERADOR DE DATASET - VAREJO ONLINE MUSICAL")
    print("=" * 60)
    
    # Gerar dataset
    df = gerar_dataset(num_produtos=40, usar_spotify=True)
    
    # Salvar arquivos
    salvar_csv(df, "dataset_varejo_musical.csv")
    salvar_ground_truth(df, "ground_truth_exemplo.csv")
    
    # Mostrar preview
    print("\n📋 Preview do Dataset:")
    print(df.head(10).to_string(index=False))
    
    # Salvar queries de exemplo
    with open("queries_exemplo.sql", "w") as f:
        f.write(EXEMPLO_QUERIES)
    print("\n✓ Arquivo 'queries_exemplo.sql' criado!")
    
    # Estatísticas
    print("\n📈 ESTATÍSTICAS DO DATASET:")
    print(f"  Total de produtos: {len(df)}")
    print(f"  Categorias: {df['categoria'].nunique()}")
    print(f"  Preço médio: R$ {df['preco_unitario'].mean():.2f}")
    print(f"  Estoque total: {df['quantidade_estoque'].sum()} unidades")
    print(f"  Valor total em estoque: R$ {(df['quantidade_estoque'] * df['preco_unitario']).sum():.2f}")
    print(f"\n  Por categoria:")
    print(df.groupby('categoria').size().to_string())
    
    print("\n✅ Dataset gerado com sucesso!\n")
