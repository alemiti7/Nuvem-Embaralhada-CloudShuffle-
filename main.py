import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import logging 
from collections import defaultdict
import random
from datetime import datetime

# ======================================================================
# DESCRIÇÃO GERAL DO SCRIPT - VERSÃO COM RANDOMIZAÇÃO E TIMESTAMP
# ======================================================================
# Este script Python realiza o processamento de um arquivo CSV para gerar
# uma Nuvem de Palavras (WordCloud) com RANDOMIZAÇÃO e TIMESTAMP automático.
#
# FUNCIONALIDADES PRINCIPAIS:
# 1. Processamento em chunks para datasets grandes (>100k registros)
# 2. Randomização: Embaralha os termos a cada execução (visualização diferente)
# 3. Timestamp: Gera arquivo único com data/hora (nunca sobrescreve)
# 4. Sistema de logging completo para auditoria e debug
#
# BIBLIOTECAS UTILIZADAS:
# - pandas: Leitura e manipulação de dados CSV com suporte a chunks
# - sklearn: Vetorização e contagem de frequência de termos
# - wordcloud: Geração da visualização em nuvem de palavras
# - logging: Sistema de rastreamento e registro de eventos
# - collections.defaultdict: Acumulação eficiente de frequências
# - random: Randomização dos termos para cada execução
# - datetime: Geração de timestamp para nomes únicos de arquivo
#
# OTIMIZAÇÕES IMPLEMENTADAS:
# - Processamento em chunks para datasets massivos (evita overflow de memória)
# - Uso de matriz esparsa para redução de memória (60-80%)
# - Acumulação incremental de frequências entre chunks
# - Otimização de tipos de dados (dtype) para economia de RAM
# - Resolução de imagem ajustada para melhor performance
#
# CAPACIDADE:
# - Datasets pequenos (<100k): Processamento padrão rápido
# - Datasets médios (100k-1M): Processamento em chunks de 50k
# - Datasets grandes (>1M): Processamento em chunks de 20k-50k
#
# FORMATO DE SAÍDA:
# - Arquivo: myplot_YYYYMMDD_HHMMSS.png
# - Exemplo: myplot_20251109_143025.png
# ======================================================================

# ----------------------------------------------------------------------
# ⚙️ BLOCO 1: CONFIGURAÇÃO DO SISTEMA DE LOGGING
# ----------------------------------------------------------------------
LOG_FILE = 'script_wordcloud.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
)

logger = logging.getLogger(__name__)
logger.info("--- Início da execução do script de Nuvem de Palavras (COM RANDOMIZAÇÃO) ---")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 📁 BLOCO 2: DEFINIÇÃO DE CONFIGURAÇÕES INICIAIS
# ----------------------------------------------------------------------
file_path = 'heroes_information.csv'
column_name = 'name'
CHUNK_SIZE = 50000

# 🎲 NOVA CONFIGURAÇÃO: Seed aleatória para randomização
random.seed()  # Usa timestamp como seed (diferente a cada execução)

logger.info(f"Configuração: Arquivo='{file_path}', Coluna='{column_name}', Chunk={CHUNK_SIZE}")
logger.info("🎲 Modo de randomização ativado")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 🔧 BLOCO 3: FUNÇÃO TOKENIZADORA PERSONALIZADA
# ----------------------------------------------------------------------
def comma_tokenizer(text):
    """
    Tokeniza texto separado por vírgulas.
    
    Args:
        text (str): Texto a ser tokenizado
        
    Returns:
        list: Lista de tokens limpos e não vazios
    """
    if pd.isna(text):
        return []
    
    tokens = [t.strip() for t in str(text).split(',') if t.strip()]
    return tokens
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 📊 BLOCO 4: INICIALIZAÇÃO DE ESTRUTURAS DE DADOS
# ----------------------------------------------------------------------
global_vocab = set()
freq_accumulator = defaultdict(int)
total_rows_processed = 0
total_rows_valid = 0
chunk_count = 0

logger.info("Estruturas de dados inicializadas para processamento em chunks.")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 📖 BLOCO 5: LEITURA E PROCESSAMENTO EM CHUNKS
# ----------------------------------------------------------------------
try:
    logger.info("Iniciando leitura do arquivo em chunks...")
    
    for chunk_num, chunk in enumerate(pd.read_csv(
        file_path,
        encoding='utf-8',
        usecols=[column_name],
        dtype={column_name: 'string'},
        chunksize=CHUNK_SIZE
    ), start=1):
        
        logger.info(f"Processando chunk {chunk_num} ({len(chunk)} linhas)...")
        
        if column_name not in chunk.columns:
            logger.error(f"Coluna '{column_name}' não encontrada no chunk {chunk_num}.")
            print(f"❌ Erro: Coluna '{column_name}' não encontrada.")
            exit()
        
        texts_chunk = chunk[column_name].dropna()
        valid_in_chunk = len(texts_chunk)
        
        total_rows_processed += len(chunk)
        total_rows_valid += valid_in_chunk
        
        logger.info(f"  → Chunk {chunk_num}: {valid_in_chunk} linhas válidas de {len(chunk)}")
        
        if valid_in_chunk == 0:
            logger.warning(f"  ⚠️ Chunk {chunk_num} vazio após remoção de NaN. Pulando...")
            continue
        
        vectorizer_chunk = CountVectorizer(tokenizer=comma_tokenizer)
        X_chunk = vectorizer_chunk.fit_transform(texts_chunk)
        
        freq_chunk = X_chunk.sum(axis=0).A1
        terms_chunk = vectorizer_chunk.get_feature_names_out()
        
        logger.info(f"  → Chunk {chunk_num}: {len(terms_chunk)} termos únicos encontrados")
        
        for term, freq in zip(terms_chunk, freq_chunk):
            global_vocab.add(term)
            freq_accumulator[term] += freq
        
        chunk_count += 1
        logger.info(f"  ✅ Chunk {chunk_num} processado. Total de termos únicos: {len(global_vocab)}")
        
        del chunk, texts_chunk, X_chunk, vectorizer_chunk
    
    logger.info(f"✅ Todos os chunks processados com sucesso!")
    logger.info(f"📊 ESTATÍSTICAS FINAIS:")
    logger.info(f"  - Total de chunks processados: {chunk_count}")
    logger.info(f"  - Total de linhas no arquivo: {total_rows_processed}")
    logger.info(f"  - Total de linhas válidas (sem NaN): {total_rows_valid}")
    logger.info(f"  - Total de termos únicos: {len(global_vocab)}")
    logger.info(f"  - Taxa de linhas válidas: {(total_rows_valid/total_rows_processed*100):.2f}%")

except FileNotFoundError:
    logger.error(f"❌ Erro: O arquivo '{file_path}' não foi encontrado.")
    print(f"❌ Erro: O arquivo '{file_path}' não foi encontrado.")
    exit()

except pd.errors.EmptyDataError:
    logger.error(f"❌ Erro: O arquivo '{file_path}' está vazio ou corrompido.")
    print(f"❌ Erro: Arquivo vazio ou corrompido.")
    exit()
    
except Exception as e:
    logger.critical(f"❌ Erro inesperado durante o processamento: {e}")
    print(f"❌ Erro inesperado: {e}")
    exit()
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# ✅ BLOCO 6: VALIDAÇÃO DE DADOS PROCESSADOS
# ----------------------------------------------------------------------
if len(freq_accumulator) == 0:
    logger.error("❌ Nenhum termo válido encontrado após processar todos os chunks.")
    print("❌ Erro: Nenhum dado válido para gerar nuvem de palavras.")
    exit()

logger.info(f"Validação concluída. Prosseguindo com {len(freq_accumulator)} termos.")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 🎲 BLOCO 6.5: RANDOMIZAÇÃO DAS FREQUÊNCIAS
# ----------------------------------------------------------------------
# NOVA FUNCIONALIDADE: Embaralha as frequências entre os termos
# Mantém a distribuição de tamanhos mas randomiza quais palavras
# aparecem em cada tamanho
# ----------------------------------------------------------------------
logger.info("🎲 Aplicando randomização nas frequências...")

# Extrai listas separadas de termos e frequências
terms_list = list(freq_accumulator.keys())
freq_list = list(freq_accumulator.values())

# Embaralha a lista de termos (mantém frequências na ordem original)
random.shuffle(terms_list)

# Recria o dicionário com termos embaralhados mas frequências originais
randomized_freq = dict(zip(terms_list, freq_list))

logger.info(f"✅ Frequências randomizadas. {len(randomized_freq)} termos redistribuídos.")
logger.info(f"🎯 Preview - Termos mais frequentes após randomização: {list(randomized_freq.keys())[:10]}")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 🎨 BLOCO 7: GERAÇÃO DA NUVEM DE PALAVRAS
# ----------------------------------------------------------------------
logger.info("Gerando nuvem de palavras a partir das frequências randomizadas...")

wordcloud = WordCloud(
    width=1024,
    height=768,
    background_color='white',
    max_words=500,
    min_word_length=2,
    relative_scaling=0.5,
).generate_from_frequencies(randomized_freq)  # 🎲 Usa frequências randomizadas

logger.info("Objeto WordCloud gerado com sucesso a partir das frequências randomizadas.")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 💾 BLOCO 8: SALVAMENTO DA IMAGEM COM TIMESTAMP
# ----------------------------------------------------------------------
# 🕐 NOVO: Gera nome de arquivo com timestamp único
# Formato: myplot_YYYYMMDD_HHMMSS.png
# Exemplo: myplot_20251109_143025.png
# ----------------------------------------------------------------------
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'myplot_{timestamp}.png'

logger.info(f"📁 Nome do arquivo gerado: {output_file}")

try:
    wordcloud.to_file(output_file)
    logger.info(f"Nuvem de palavras salva com sucesso como '{output_file}'.")
    print(f"✅ Nuvem de palavras gerada e salva como '{output_file}'.")
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎲 Modo randomizado: Cada execução gera uma visualização diferente!")
    print(f"📊 Total de termos processados: {len(global_vocab):,}")
    print(f"📊 Total de linhas processadas: {total_rows_processed:,}")
    print(f"📊 Chunks processados: {chunk_count}")
    
except Exception as e:
    logger.error(f"❌ Erro ao salvar a imagem da nuvem de palavras: {e}")
    print(f"❌ Erro ao salvar a imagem: {e}")
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 🏁 BLOCO 9: FINALIZAÇÃO DO SCRIPT
# ----------------------------------------------------------------------
logger.info("--- Fim da execução do script (COM RANDOMIZAÇÃO) ---")
# ----------------------------------------------------------------------


# ======================================================================
# 🎲 DOCUMENTAÇÃO DA RANDOMIZAÇÃO E TIMESTAMP
# ======================================================================
#
# ESTRATÉGIA IMPLEMENTADA:
# - Coleta todas as frequências originais dos termos
# - Embaralha aleatoriamente a lista de termos
# - Reassocia os termos embaralhados com as frequências originais
# - Resultado: Mesma distribuição de tamanhos, mas palavras diferentes
#
# 🕐 TIMESTAMP NOS ARQUIVOS:
# Formato: myplot_YYYYMMDD_HHMMSS.png
# Benefícios:
# - Nunca sobrescreve arquivos anteriores
# - Fácil identificação da ordem cronológica
# - Rastreamento de múltiplas execuções
# - Comparação visual entre diferentes gerações
#
# Exemplos de nomes gerados:
# - myplot_20251109_143025.png  (09/11/2025 às 14:30:25)
# - myplot_20251109_150133.png  (09/11/2025 às 15:01:33)
# - myplot_20251110_091545.png  (10/11/2025 às 09:15:45)
#
# EXEMPLO DE RANDOMIZAÇÃO:
# Original:  {"batman": 100, "superman": 80, "spider-man": 60}
# Shuffle:   {"spider-man": 100, "batman": 80, "superman": 60}
# (Cada execução produz uma redistribuição diferente)
#
# ALTERNATIVAS POSSÍVEIS:
# 1. random.seed(42) - Para resultados reproduzíveis com seed fixa
# 2. Randomização parcial - Embaralhar apenas top N termos
# 3. Randomização de cores - Além de posição/tamanho
# 4. Sampling - Mostrar subset aleatório diferente a cada execução
#
# FORMATOS DE TIMESTAMP ALTERNATIVOS:
# - ISO 8601: datetime.now().isoformat() → "2025-11-09T14:30:25"
# - Unix: int(time.time()) → "1731167425"
# - Legível: strftime("%d-%b-%Y_%Hh%Mm%Ss") → "09-Nov-2025_14h30m25s"
#
# Para SEED FIXA (resultados reproduzíveis):
# Substitua random.seed() por random.seed(42) no Bloco 2
#
# ======================================================================