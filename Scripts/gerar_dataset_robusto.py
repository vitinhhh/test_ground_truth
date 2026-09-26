#!/usr/bin/env python3
"""
Gerador de Dataset Robusto para Busca Híbrida
Cria 500+ produtos musicais com descrições longas, reviews, e tags

Requisitos:
    pip install faker pandas

Uso:
    python gerar_dataset_robusto.py
"""

import pandas as pd
from faker import Faker
import random
import json
from datetime import datetime, timedelta

# ============================================
# CONFIGURAÇÃO
# ============================================

NUM_PRODUTOS = 500
faker = Faker('pt_BR')

# ============================================
# DADOS DE CATÁLOGO
# ============================================

CATEGORIAS = {
    "Instrumentos": {
        "produtos": [
            "Guitarra Acústica", "Guitarra Elétrica", "Violão Clássico",
            "Teclado Sintetizador", "Piano Digital", "Bateria Acústica",
            "Bateria Eletrônica", "Saxofone Alto", "Saxofone Tenor",
            "Trompete", "Clarinete", "Flauta Transversal", "Flauta Doce",
            "Baixo Elétrico", "Violino", "Viola de Arco", "Violoncelo",
            "Acordeão", "Harmônica", "Ukulele", "Bandolim", "Cavaquinho",
            "Tambor", "Bumbo", "Pratos", "Pandeiro", "Surdo", "Agogô",
            "Cuíca", "Caxixi", "Kalimba", "Didgeridoo", "Theremin"
        ],
        "descricao_template": "Um excelente {produto} para músicos profissionais e iniciantes. Este instrumento oferece som de qualidade superior com construção robusta e acabamento premium. Ideal para estúdios de gravação, apresentações ao vivo e aulas de música. Feito com materiais de alta qualidade, garante durabilidade e excelente resposta sonora. Certificado e testado antes do envio. Perfeito para quem busca qualidade e confiabilidade."
    },
    "Acessórios": {
        "produtos": [
            "Baqueta de Madeira", "Baqueta de Nylon", "Plectro de Aço",
            "Plectro de Celulose", "Corda de Aço", "Corda de Nylon",
            "Correia de Couro", "Correia de Nylon", "Capa Protetora",
            "Estojo Rígido", "Estojo de Transporte", "Capotrasto",
            "Afinador Digital", "Metrônomo", "Stand para Guitarra",
            "Stand para Teclado", "Pedal de Volume", "Pedal Sustain",
            "Amplificador para Fone", "Controlador MIDI", "Pad MIDI",
            "Humidificador", "Limpador de Cordas", "Desoxidante",
            "Almofada para Fone", "Cabos XLR", "Cabos RCA",
            "Adaptadores Áudio", "Suporte para Partitura", "Luz LED"
        ],
        "descricao_template": "Acessório indispensável {produto} para músicos. Oferece qualidade profissional e durabilidade garantida. Compatível com diversos instrumentos musicais. Perfeito para estúdio, apresentações e prática diária. Construído com materiais premium que garantem excelente funcionalidade. Recomendado por músicos profissionais. Fácil de usar e manter."
    },
    "Equipamentos de Áudio": {
        "produtos": [
            "Interface de Áudio USB", "Interface Thunderbolt", "Placa de Som Externa",
            "Microfone Condensador", "Microfone Dinâmico", "Microfone USB",
            "Fone Over-Ear", "Fone In-Ear", "Fone Estéreo",
            "Monitor de Estúdio", "Alto-Falante Ativo", "Amplificador de Potência",
            "Mixer Analógico", "Mixer Digital", "Processador de Efeitos",
            "Reverberador", "Equalizador Gráfico", "Compressor de Áudio",
            "Preamp Válvula", "Gravador Digital", "Recorder Portátil",
            "Cabeçote de Amplificador", "Pedal Board", "Case para Equipamento",
            "Suporte Profissional", "Isolador Acústico", "Difusor de Som"
        ],
        "descricao_template": "Equipamento profissional {produto} de alta qualidade para produção musical. Oferece som cristalino e performance confiável em qualquer ambiente. Ideal para estúdios, salas de concerto e casas de shows. Construído com tecnologia de ponta e componentes de qualidade superior. Recomendado por engenheiros de som e produtores musicais. Garante excelentes resultados em gravações e apresentações."
    },
    "Software Musical": {
        "produtos": [
            "DAW Profissional", "Sequenciador MIDI", "Sintetizador Software",
            "Sampler Digital", "Biblioteca de Samples", "Plug-in de Efeitos",
            "Plug-in de Síntese", "Editor de Áudio", "Mastering Software",
            "Notation Software", "Acordeador Automático", "Metrônomo Digital",
            "Tuner Software", "Analisador Espectral", "Gravador Multipista",
            "Editor de Vídeo Musical", "Looper Software", "Arpeggiador",
            "Quantizador Automático", "Harmônicos Gerador", "Convolver de Áudio"
        ],
        "descricao_template": "Software musical profissional {produto} com recursos avançados de produção. Oferece ferramentas poderosas para compositores e produtores. Interface intuitiva e compatível com diversos formatos. Perfeito para criação, edição e masterização de áudio. Suporte técnico e atualizações contínuas. Recomendado pela comunidade musical internacional."
    }
}

MARCAS_POR_CATEGORIA = {
    "Instrumentos": ["Yamaha", "Fender", "Gibson", "Ibanez", "Marshall", "Boss", "Pearl", "Ludwig", "Tama", "Zildjian", "Sabian", "Selmer", "Buffet", "Thomann", "Korg", "Casio", "Roland", "Behringer"],
    "Acessórios": ["Vic Firth", "Ernie Ball", "D'Addario", "Elixir", "GHS", "Dunlop", "Fender", "Shubb", "Korg", "Boss", "Zoom"],
    "Equipamentos de Áudio": ["Shure", "Neumann", "Audio-Technica", "Sony", "Sennheiser", "Rode", "Focusrite", "Universal Audio", "Presonus", "Behringer", "Yamaha", "Pioneer", "Technics"],
    "Software Musical": ["Ableton", "Logic Pro", "Pro Tools", "Cubase", "Reaper", "Bitwig", "FL Studio", "Studio One", "Reason", "Nuendo"]
}

TAGS_POR_CATEGORIA = {
    "Instrumentos": ["profissional", "iniciante", "estúdio", "concert", "portátil", "alta-qualidade", "garantia", "som-profissional", "construção-robusta", "acabamento-premium"],
    "Acessórios": ["essencial", "durável", "compatível", "profissional", "prático", "premium", "ergonômico", "recomendado", "confiável", "versátil"],
    "Equipamentos de Áudio": ["profissional", "estúdio", "cristalino", "confiável", "tecnologia-ponta", "engenheiros-recomenda", "alta-qualidade", "precisão", "versatilidade", "premium"],
    "Software Musical": ["profissional", "avançado", "intuitivo", "compatível", "poderoso", "análise-espectral", "masterização", "gravação", "edição", "produção"]
}

FAIXA_PRECO = {
    "Instrumentos": (200, 5000),
    "Acessórios": (10, 500),
    "Equipamentos de Áudio": (150, 3000),
    "Software Musical": (50, 500)
}

# ============================================
# FUNÇÕES GERADORAS
# ============================================

def gerar_descricao_detalhada(categoria, produto, marca):
    """Gera descrição longa e detalhada"""
    template = CATEGORIAS[categoria]["descricao_template"]
    descricao_base = template.format(produto=produto)
    
    # Adiciona mais detalhes
    detalhes = [
        f"Marca: {marca}. ",
        "Oferece compatibilidade com múltiplos sistemas operacionais. ",
        "Inclui manual de instruções detalhado em português. ",
        "Suporte técnico disponível 24/7. ",
        "Produto original com nota fiscal e garantia de fábrica. ",
        "Testado rigorosamente antes do envio. ",
        "Recomendado por especialistas da área. ",
        "Excelente custo-benefício. ",
        "Fácil de usar e manter. ",
        "Desempenho consistente e confiável. "
    ]
    
    descricao_expandida = descricao_base + " ".join(random.sample(detalhes, k=random.randint(4, 6)))
    return descricao_expandida

def gerar_reviews_simulados(num_reviews=3):
    """Gera reviews simulados"""
    reviews = []
    textos_review = [
        "Produto excelente, chegou rápido e bem embalado.",
        "Qualidade premium, recomendo para todos os músicos.",
        "Sonho realizado! Superou minhas expectativas.",
        "Profissional, durável e confiável. Muito bom!",
        "Perfeito para estúdio e apresentações. Ótimo custo-benefício.",
        "Construção sólida, som cristalino e resposta rápida.",
        "Investimento que vale a pena. Produto de alta qualidade.",
        "Atendimento excelente e produto de primeira qualidade.",
        "Ideal para profissionais e iniciantes. Muito versátil.",
        "Recomendo fortemente. Melhor compra do ano!",
        "Compatibilidade perfeita com meus equipamentos.",
        "Embalagem profissional, produto impecável.",
        "Excelente relação qualidade-preço.",
        "Produto confiável para uso contínuo.",
        "Suporte técnico muito responsivo e atencioso."
    ]
    
    for _ in range(num_reviews):
        reviews.append({
            "texto": random.choice(textos_review),
            "rating": random.randint(4, 5),
            "data": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
        })
    
    return json.dumps(reviews, ensure_ascii=False)

def gerar_especificacoes(categoria, produto):
    """Gera especificações técnicas"""
    specs = {
        "Instrumentos": {
            "Material": random.choice(["Madeira de Lei", "Mogno", "Spruce", "Aço", "Latão", "Níquel"]),
            "Peso": f"{random.randint(1, 10)} kg",
            "Cor": random.choice(["Preto", "Branco", "Natural", "Sunburst", "Vermelho", "Azul"]),
            "Garantia": f"{random.randint(1, 5)} anos"
        },
        "Acessórios": {
            "Material": random.choice(["Nylon", "Aço", "Madeira", "Couro", "Celulose", "Borracha"]),
            "Comprimento": f"{random.randint(50, 200)} cm",
            "Peso": f"{round(random.uniform(0.1, 2), 1)} kg",
            "Compatibilidade": "Universal"
        },
        "Equipamentos de Áudio": {
            "Frequência": f"{random.randint(20, 100)}-{random.randint(10000, 20000)} Hz",
            "Impedância": f"{random.randint(4, 600)} Ohm",
            "Sensibilidade": f"{random.randint(80, 110)} dB",
            "Conexão": random.choice(["USB", "XLR", "RCA", "3.5mm", "Bluetooth"])
        },
        "Software Musical": {
            "Sistema": random.choice(["Windows/Mac", "Mac/Linux", "Windows/Mac/Linux", "Cloud"]),
            "Processamento": f"{random.randint(32, 256)} bit",
            "Taxa de Amostragem": f"até {random.randint(44, 192)} kHz",
            "Licença": "Perpétua" if random.random() > 0.5 else "Anual"
        }
    }
    
    return json.dumps(specs.get(categoria, {}), ensure_ascii=False)

def gerar_dataset_robusto(num_produtos):
    """Gera dataset com múltiplas categorias"""
    
    print(f"\n{'=' * 80}")
    print(f"GERANDO DATASET ROBUSTO COM {num_produtos} PRODUTOS")
    print(f"{'=' * 80}\n")
    
    produtos_lista = []
    contador = 0
    
    for categoria in CATEGORIAS.keys():
        print(f"📝 Gerando produtos da categoria: {categoria}")
        
        # Distribuir produtos entre categorias
        produtos_categoria = max(1, num_produtos // len(CATEGORIAS))
        
        for _ in range(produtos_categoria):
            if contador >= num_produtos:
                break
            
            contador += 1
            
            produto_nome = random.choice(CATEGORIAS[categoria]["produtos"])
            marca = random.choice(MARCAS_POR_CATEGORIA[categoria])
            preco_min, preco_max = FAIXA_PRECO[categoria]
            
            produto = {
                "produto_id": contador,
                "nome_produto": f"{marca} {produto_nome}",
                "categoria": categoria,
                "marca": marca,
                "descricao_longa": gerar_descricao_detalhada(categoria, produto_nome, marca),
                "preco_unitario": round(random.uniform(preco_min, preco_max), 2),
                "quantidade_estoque": random.randint(0, 100),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "num_reviews": random.randint(5, 200),
                "reviews": gerar_reviews_simulados(num_reviews=random.randint(2, 5)),
                "tags": ",".join(random.sample(TAGS_POR_CATEGORIA[categoria], k=random.randint(3, 6))),
                "especificacoes": gerar_especificacoes(categoria, produto_nome),
                "fornecedor": faker.company(),
                "sku": f"{marca[:3].upper()}-{categoria[:4].upper()}-{contador:04d}",
                "status": "ativo" if random.random() > 0.1 else "inativo",
                "data_adicao": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
            }
            
            produtos_lista.append(produto)
            
            if contador % 100 == 0:
                print(f"  ✓ {contador} produtos gerados...")
    
    df = pd.DataFrame(produtos_lista)
    
    print(f"\n✅ {len(df)} produtos gerados com sucesso!\n")
    
    return df

# ============================================
# SALVAR DADOS
# ============================================

def salvar_dataset(df, nome_arquivo="dataset_robusto_500produtos.csv"):
    """Salva dataset em CSV"""
    df.to_csv(nome_arquivo, index=False)
    print(f"💾 Dataset salvo: {nome_arquivo}")
    print(f"   Tamanho: {len(df)} linhas × {len(df.columns)} colunas")
    print(f"   Arquivo: {nome_arquivo}\n")

def gerar_relatorio(df):
    """Gera relatório de estatísticas"""
    print(f"{'=' * 80}")
    print(f"ESTATÍSTICAS DO DATASET")
    print(f"{'=' * 80}\n")
    
    print(f"RESUMO GERAL:")
    print(f"  Total de produtos: {len(df)}")
    print(f"  Categorias: {df['categoria'].nunique()}")
    print(f"  Marcas: {df['marca'].nunique()}\n")
    
    print(f"POR CATEGORIA:")
    for categoria, count in df['categoria'].value_counts().items():
        print(f"  {categoria}: {count}")
    print()
    
    print(f"ANÁLISE DE PREÇOS:")
    print(f"  Mínimo: R$ {df['preco_unitario'].min():.2f}")
    print(f"  Máximo: R$ {df['preco_unitario'].max():.2f}")
    print(f"  Média: R$ {df['preco_unitario'].mean():.2f}")
    print(f"  Total em estoque: R$ {(df['preco_unitario'] * df['quantidade_estoque']).sum():.2f}\n")
    
    print(f"ANÁLISE DE ESTOQUE:")
    print(f"  Total de unidades: {df['quantidade_estoque'].sum()}")
    print(f"  Média por produto: {df['quantidade_estoque'].mean():.1f}")
    print(f"  Produtos sem estoque: {len(df[df['quantidade_estoque'] == 0])}\n")
    
    print(f"ANÁLISE DE RATINGS:")
    print(f"  Rating médio: {df['rating'].mean():.2f}")
    print(f"  Reviews totais: {df['num_reviews'].sum()}")
    print(f"  Reviews médios: {df['num_reviews'].mean():.0f}\n")
    
    print(f"CAMPOS DISPONÍVEIS:")
    for col in df.columns:
        print(f"  • {col}")
    print()

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    
    print(f"\n{'#' * 80}")
    print(f"# GERADOR DE DATASET ROBUSTO PARA BUSCA HÍBRIDA")
    print(f"# 500+ Produtos Musicais com Descrições Detalhadas")
    print(f"{'#' * 80}\n")
    
    # Gerar dataset
    df = gerar_dataset_robusto(NUM_PRODUTOS)
    
    # Gerar relatório
    gerar_relatorio(df)
    
    # Salvar
    salvar_dataset(df)
    
    print(f"{'=' * 80}")
    print(f"✅ DATASET PRONTO PARA USO!")
    print(f"{'=' * 80}\n")
    
    print(f"Próximos passos:")
    print(f"  1. Importar em MySQL: python 02_importar_e_testar.py")
    print(f"  2. Criar Ground Truth: mysql < ground_truth_busca_hibrida.sql")
    print(f"  3. Implementar buscas (lexical, semântica, híbrida)")
    print(f"  4. Calcular métricas: python calcular_mmr.py\n")
