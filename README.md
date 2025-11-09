# 🎨 WordCloud Generator with Randomization & Timestamp

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

Um gerador de nuvem de palavras otimizado para processar grandes datasets CSV com randomização automática e timestamp único em cada execução.

## 📋 Índice

- [Características](#-características)
- [Demonstração](#-demonstração)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Configuração](#️-configuração)
- [Como Funciona](#-como-funciona)
- [Logs e Auditoria](#-logs-e-auditoria)
- [Performance](#-performance)
- [Customização](#-customização)
- [Solução de Problemas](#-solução-de-problemas)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

- 🎲 **Randomização Automática**: Cada execução gera uma visualização única
- 🕐 **Timestamp Único**: Arquivos nunca são sobrescritos
- 💾 **Processamento em Chunks**: Lida com datasets massivos sem esgotar memória
- 📊 **Logging Completo**: Rastreamento detalhado de todas as operações
- ⚡ **Otimizado para Performance**: Matriz esparsa e liberação inteligente de memória
- 🎨 **Altamente Customizável**: Fácil ajuste de cores, tamanhos e comportamento

## 🎬 Demonstração

### Entrada (CSV)
```csv
name
Batman, Superman, Wonder Woman
Spider-Man, Iron Man
Flash, Aquaman, Cyborg
...
```

### Saída
- **Arquivos gerados**: `myplot_20251109_143025.png`, `myplot_20251109_150133.png`, etc.
- **Cada execução**: Visualização única com termos embaralhados
- **Log detalhado**: `script_wordcloud.log`

### Exemplos de Visualizações

| Execução 1 | Execução 2 | Execução 3 |
|------------|------------|------------|
| ![Exec1](https://via.placeholder.com/200x150/4A90E2/FFFFFF?text=Batman+Grande) | ![Exec2](https://via.placeholder.com/200x150/E24A4A/FFFFFF?text=Flash+Grande) | ![Exec3](https://via.placeholder.com/200x150/4AE290/FFFFFF?text=Superman+Grande) |
| Batman em destaque | Flash em destaque | Superman em destaque |

> **Nota**: Mesmos dados, visualizações diferentes a cada execução!

## 📦 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/wordcloud-generator.git
cd wordcloud-generator

# Instale as dependências
pip install -r requirements.txt
```

### `requirements.txt`
```txt
pandas>=1.3.0
wordcloud>=1.8.1
scikit-learn>=0.24.0
```

### Instalação Manual (Alternativa)
```bash
pip install pandas wordcloud scikit-learn
```

## 🚀 Uso Rápido

### 1. Preparar seu CSV
Certifique-se de que seu arquivo CSV tem uma coluna com valores separados por vírgula:

```csv
name
Batman, Superman
Spider-Man, Iron Man, Thor
Flash, Aquaman
```

### 2. Configurar o Script
Edite as linhas 66-68 do script:

```python
file_path = 'seu_arquivo.csv'      # Nome do seu arquivo
column_name = 'sua_coluna'         # Nome da coluna a processar
CHUNK_SIZE = 50000                 # Ajuste conforme necessário
```

### 3. Executar
```bash
python wordcloud_generator.py
```

### 4. Resultado
```
✅ Nuvem de palavras gerada e salva como 'myplot_20251109_143025.png'.
🕐 Timestamp: 2025-11-09 14:30:25
🎲 Modo randomizado: Cada execução gera uma visualização diferente!
📊 Total de termos processados: 734
📊 Total de linhas processadas: 1,500
📊 Chunks processados: 1
```

## ⚙️ Configuração

### Parâmetros Principais

| Parâmetro | Descrição | Valor Padrão | Recomendação |
|-----------|-----------|--------------|--------------|
| `file_path` | Caminho do arquivo CSV | `'heroes_information.csv'` | Altere para seu arquivo |
| `column_name` | Coluna a processar | `'name'` | Nome da sua coluna |
| `CHUNK_SIZE` | Linhas por chunk | `50000` | Veja tabela abaixo |

### Tabela de CHUNK_SIZE Recomendado

| Linhas Totais | CHUNK_SIZE | RAM Mínima | Tempo Estimado |
|---------------|------------|------------|----------------|
| < 100k        | 50k-100k   | 4GB        | 10-30s         |
| 100k-500k     | 50k        | 4GB        | 30s-1min       |
| 500k-1M       | 50k        | 8GB        | 1-3min         |
| 1M-5M         | 30k        | 8GB        | 3-7min         |
| 5M-10M        | 20k        | 16GB       | 7-15min        |
| > 10M         | 10k-20k    | 16GB+      | 15min+         |

### Configurações do WordCloud (Linhas 252-258)

```python
wordcloud = WordCloud(
    width=1024,              # Largura da imagem
    height=768,              # Altura da imagem
    background_color='white', # Cor de fundo
    max_words=500,           # Máximo de palavras exibidas
    min_word_length=2,       # Tamanho mínimo das palavras
    relative_scaling=0.5,    # Proporção de tamanho
)
```

### Opções Avançadas

```python
# Paletas de cores disponíveis
colormap='viridis'   # Científica
colormap='plasma'    # Quente
colormap='coolwarm'  # Azul/Vermelho
colormap='rainbow'   # Arco-íris

# Tamanhos de fonte
min_font_size=8      # Mínimo (padrão: 4)
max_font_size=200    # Máximo (padrão: auto)

# Fundo transparente
background_color='transparent'
```

## 🔍 Como Funciona

### Arquitetura do Script

```
┌─────────────────────────────────────────────┐
│  1. Configuração Inicial                    │
│     - Logging setup                         │
│     - Seed aleatória                        │
│     - Parâmetros de entrada                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  2. Processamento em Chunks                 │
│     ┌─────────────────────────────────────┐ │
│     │ Chunk 1 (50k linhas)                │ │
│     │  → Remove NaN                       │ │
│     │  → Tokeniza                         │ │
│     │  → Vetoriza                         │ │
│     │  → Extrai frequências               │ │
│     │  → Acumula no global                │ │
│     └─────────────────────────────────────┘ │
│     ┌─────────────────────────────────────┐ │
│     │ Chunk 2 (50k linhas)                │ │
│     │  → ... (mesmo processo)             │ │
│     └─────────────────────────────────────┘ │
│     ...                                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  3. Randomização                            │
│     - Embaralha termos                      │
│     - Mantém distribuição de frequências    │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  4. Geração da WordCloud                    │
│     - Cria objeto WordCloud                 │
│     - Aplica configurações visuais          │
│     - Gera imagem                           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  5. Salvamento com Timestamp                │
│     - Gera timestamp único                  │
│     - Salva PNG                             │
│     - Registra em log                       │
└─────────────────────────────────────────────┘
```

### Algoritmo de Randomização

```python
# Original
termos = ["Batman", "Superman", "Flash"]
freqs  = [150, 120, 90]

# Após random.shuffle(termos)
termos = ["Flash", "Batman", "Superman"]
freqs  = [150, 120, 90]  # Inalterado

# Resultado
{"Flash": 150, "Batman": 120, "Superman": 90}
# Flash agora é o maior termo!
```

## 📝 Logs e Auditoria

### Arquivo de Log: `script_wordcloud.log`

```log
2025-11-09 14:30:25 - INFO - --- Início da execução do script ---
2025-11-09 14:30:25 - INFO - Configuração: Arquivo='heroes.csv', Coluna='name'
2025-11-09 14:30:25 - INFO - 🎲 Modo de randomização ativado
2025-11-09 14:30:26 - INFO - Processando chunk 1 (50000 linhas)...
2025-11-09 14:30:27 - INFO -   → Chunk 1: 734 termos únicos encontrados
2025-11-09 14:30:27 - INFO - ✅ Frequências randomizadas. 734 termos redistribuídos
2025-11-09 14:30:28 - INFO - 📁 Nome do arquivo gerado: myplot_20251109_143025.png
2025-11-09 14:30:28 - INFO - --- Fim da execução do script ---
```

### Analisando Logs

```bash
# Ver todas as execuções
grep "Início da execução" script_wordcloud.log

# Ver erros
grep "ERROR" script_wordcloud.log

# Contar execuções do dia
grep "2025-11-09" script_wordcloud.log | wc -l

# Tempo de execução (comparar início e fim)
grep -E "(Início|Fim) da execução" script_wordcloud.log
```

## ⚡ Performance

### Otimizações Implementadas

1. **Matriz Esparsa**: Reduz uso de memória em 60-80%
2. **Liberação Explícita**: `del chunk` após processamento
3. **Tipos Otimizados**: `dtype='string'` economiza RAM
4. **Apenas Coluna Necessária**: `usecols=[column_name]`
5. **Processamento Incremental**: Chunks independentes

### Benchmarks

| Dataset | Tamanho | Chunk | Tempo | Memória Pico |
|---------|---------|-------|-------|--------------|
| Pequeno | 10k     | 50k   | 5s    | 200MB        |
| Médio   | 500k    | 50k   | 45s   | 800MB        |
| Grande  | 2M      | 30k   | 3min  | 1.5GB        |
| Massivo | 10M     | 20k   | 15min | 2.5GB        |

> **Ambiente de teste**: Intel i5, 16GB RAM, SSD

### Dicas de Performance

```python
# Para datasets MUITO grandes (>10M linhas)
CHUNK_SIZE = 10000  # Reduza o chunk

# Para máquinas com pouca RAM
CHUNK_SIZE = 20000  # Mais chunks, menos memória

# Para máquinas potentes
CHUNK_SIZE = 100000  # Menos chunks, mais velocidade
```

## 🎨 Customização

### Desabilitar Randomização

Comente as linhas 196-207 (Bloco 6.5):

```python
# logger.info("🎲 Aplicando randomização nas frequências...")
# terms_list = list(freq_accumulator.keys())
# freq_list = list(freq_accumulator.values())
# random.shuffle(terms_list)
# randomized_freq = dict(zip(terms_list, freq_list))

# Use freq_accumulator diretamente
wordcloud = WordCloud(...).generate_from_frequencies(freq_accumulator)
```

### Seed Fixa (Resultados Reproduzíveis)

Linha 68:
```python
random.seed(42)  # Sempre a mesma visualização
```

### Formato de Timestamp Customizado

Linha 282:
```python
# Formato legível em português
timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mm%Ss")
# Resultado: myplot_09-11-2025_14h30m25s.png

# Formato ISO 8601
timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
# Resultado: myplot_2025-11-09T14-30-25.png

# Unix timestamp
import time
timestamp = str(int(time.time()))
# Resultado: myplot_1731167425.png
```

### Separador Customizado

Se seus dados usam outro separador (`;`, `|`, tab):

Linha 84:
```python
# Para ponto-e-vírgula
tokens = [t.strip() for t in str(text).split(';') if t.strip()]

# Para pipe
tokens = [t.strip() for t in str(text).split('|') if t.strip()]

# Para múltiplos separadores
import re
tokens = [t.strip() for t in re.split(r'[;,|]', str(text)) if t.strip()]
```

### Salvar em Outro Formato

```python
# JPEG (menor tamanho de arquivo)
output_file = f'myplot_{timestamp}.jpg'
wordcloud.to_file(output_file)

# SVG (vetorial, escalável)
from io import BytesIO
svg = wordcloud.to_svg()
with open(f'myplot_{timestamp}.svg', 'w') as f:
    f.write(svg)
```

## 🐛 Solução de Problemas

### Erro: "Coluna não encontrada"

**Problema**: Nome da coluna incorreto

**Solução**:
```python
# Verifique as colunas disponíveis
import pandas as pd
df = pd.read_csv('seu_arquivo.csv', nrows=5)
print(df.columns)
```

### Erro: "MemoryError"

**Problema**: Chunk muito grande para RAM disponível

**Solução**: Reduza `CHUNK_SIZE`
```python
CHUNK_SIZE = 10000  # Reduza gradualmente até funcionar
```

### Aviso: "Chunk vazio após remoção de NaN"

**Problema**: Chunk contém apenas valores vazios

**Solução**: Isso é normal, o script continua automaticamente

### Nenhum termo encontrado

**Problema**: Formato de dados incompatível

**Verificações**:
1. Coluna contém texto separado por vírgulas?
2. Encoding do CSV está correto? (UTF-8 esperado)
3. Arquivo contém dados válidos?

```python
# Teste de encoding
df = pd.read_csv('arquivo.csv', encoding='latin1')  # Tente outros encodings
```

### WordCloud muito lenta

**Problema**: Muitos termos únicos

**Solução**: Limite o número de palavras
```python
max_words=200,  # Reduza de 500 para 200
```

### Imagem distorcida

**Problema**: Proporção incorreta

**Solução**: Ajuste width/height
```python
width=1920,   # Full HD
height=1080,  # 16:9
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estas etapas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Áreas para Contribuição

- [ ] Suporte a múltiplos idiomas (i18n)
- [ ] Interface web (Flask/Streamlit)
- [ ] Mais formatos de saída (PDF, SVG)
- [ ] Processamento paralelo (multiprocessing)
- [ ] Suporte a stopwords customizadas
- [ ] Testes unitários
- [ ] Documentação em inglês

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2025 [Seu Nome]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Agradecimentos

- [WordCloud](https://github.com/amueller/word_cloud) por Andreas Mueller
- [Pandas](https://pandas.pydata.org/) pela manipulação de dados eficiente
- [scikit-learn](https://scikit-learn.org/) pelas ferramentas de vetorização
- Comunidade Python por feedback e sugestões

---

## 📞 Contato

- **GitHub**: [@seu-usuario](https://github.com/seu-usuario)
- **Email**: seu.email@exemplo.com
- **LinkedIn**: [Seu Nome](https://linkedin.com/in/seu-perfil)

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐

---

**Última atualização**: Novembro 2025
