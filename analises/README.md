# Análise de Dados - Mari Doutorado

Projeto de análise de dados de atendimentos médicos convertido de Jupyter Notebook para módulos Python executáveis.

## 📁 Estrutura do Projeto

```
analises/
├── config.py              # Configurações e constantes
├── utils.py               # Funções utilitárias
├── analise_urgenza.py     # Análises de Categoria Urgenza
├── analise_geral.py       # Análises gerais complementares
├── main.py                # Script principal
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

## 🚀 Como Usar

### Instalação

1. Clone o repositório ou copie os arquivos para seu servidor
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Execução

#### Modo 1: Análise Completa com Gráficos Interativos

```bash
python main.py
```

Este modo executa todas as análises e exibe os gráficos na tela.

#### Modo 2: Análise Completa Salvando Gráficos

```bash
python main.py --salvar ./output
```

Salva todos os gráficos no diretório especificado (padrão: `./output`).

#### Modo 3: Análise Rápida (Apenas Estatísticas)

```bash
python main.py --rapido
```

Executa apenas as análises estatísticas, sem gerar gráficos.

## 📊 Análises Disponíveis

### 1. Análise de Categoria Urgenza

- Distribuição de frequências e percentuais
- Gráficos de barras (absoluto e percentual)
- Gráfico de pizza
- Análise cruzada com Sottogruppo Pazienti
- Heatmap de categorias
- Evolução temporal
- Análise por faixa etária
- Resumo executivo

### 2. Análises Gerais

- Modalità Dimissione
- Problema Principale
- Pacientes frequentes
- Análise temporal
- Estatísticas de idade
- Relatório geral consolidado

## 🔧 Configuração

### Caminhos dos Dados

Edite `config.py` para ajustar os caminhos dos arquivos CSV:

```python
CAMINHO_2022 = "../dados/csv/2022"
CAMINHO_2023 = "../dados/csv/2023"
CAMINHO_2024 = "../dados/csv/2024"
```

### Personalização de Cores

As cores das categorias de urgência podem ser ajustadas em `config.py`:

```python
CORES_URGENZA = {
    'Bianca': '#E8E8E8',
    'Verde': '#2ECC71',
    'Gialla': '#F1C40F',
    'Arancione': '#E67E22',
    'Rossa': '#E74C3C'
}
```

## 📦 Módulos

### `config.py`

Contém todas as configurações globais:
- Caminhos de arquivos
- Configurações de visualização
- Cores e paletas
- Ordens de categorias
- Mapeamentos

### `utils.py`

Funções auxiliares:
- `configurar_ambiente()`: Configura matplotlib e pandas
- `carrega_dados()`: Carrega múltiplos CSVs
- `preparar_dataframe()`: Limpa e transforma dados
- `criar_subcategoria()`: Cria categorias de pacientes
- `criar_categoria_urgenza()`: Mapeia códigos de urgência
- `criar_features_temporais()`: Cria features de data/tempo
- `criar_faixa_etaria()`: Cria faixas etárias

### `analise_urgenza.py`

Análises específicas de Categoria Urgenza:
- Estatísticas descritivas
- Geração de gráficos
- Análises cruzadas
- Heatmaps
- Evolução temporal
- Resumos executivos

### `analise_geral.py`

Análises complementares:
- Modalità Dimissione
- Problema Principale
- Pacientes frequentes
- Análises temporais
- Estatísticas de idade
- Relatórios consolidados

### `main.py`

Script principal que orquestra todas as análises.

## 🌐 Hospedagem em Servidor

### Opção 1: Script Cron

Configure um cron job para executar periodicamente:

```bash
# Executar todos os dias às 2:00 AM
0 2 * * * cd /caminho/para/analises && python main.py --salvar /var/www/html/graficos
```

### Opção 2: API Flask (Exemplo)

Crie um arquivo `app.py`:

```python
from flask import Flask, jsonify
import pandas as pd
from main import executar_analise_rapida

app = Flask(__name__)

@app.route('/analise')
def executar_analise():
    try:
        df = executar_analise_rapida()
        return jsonify({
            'status': 'success',
            'total_atendimentos': len(df),
            'total_pacientes': df['Paziente'].nunique()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Execute:

```bash
python app.py
```

### Opção 3: Dashboard Interativo com Dash (Avançado)

Para criar um dashboard web interativo, adicione `dash` e `plotly` ao `requirements.txt` e crie uma interface web.

## 🔍 Exemplo de Uso Programático

```python
from config import CAMINHO_2022, CAMINHO_2023, CAMINHO_2024
from utils import configurar_ambiente, carrega_dados, preparar_dataframe
from analise_urgenza import estatisticas_urgenza

# Configurar
configurar_ambiente()

# Carregar dados
df_2022 = carrega_dados(CAMINHO_2022)
df_2023 = carrega_dados(CAMINHO_2023)
df_2024 = carrega_dados(CAMINHO_2024)

import pandas as pd
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# Preparar
df = preparar_dataframe(df)

# Analisar
stats = estatisticas_urgenza(df)
print(stats['resumo'])
```

## 📊 Outputs

### Gráficos Salvos (modo `--salvar`)

- `urgenza_barras.png`: Gráficos de barras de urgência
- `urgenza_pizza.png`: Gráfico de pizza de urgência
- `urgenza_subgrupo_heatmap.png`: Heatmap urgência x subgrupo
- `urgenza_temporal.png`: Evolução temporal da urgência

### Dados Retornados

Todas as funções retornam dicionários ou DataFrames com os resultados das análises, permitindo uso programático.

## ⚙️ Requisitos do Sistema

- Python 3.8+
- 4GB RAM mínimo (recomendado 8GB)
- 500MB espaço em disco para dados
- Sistema operacional: Windows, Linux ou macOS

## 📝 Notas

- Os dados devem estar em formato CSV
- As colunas esperadas são as mesmas do notebook original
- Para grandes volumes de dados, considere usar `executar_analise_rapida()` para evitar gráficos pesados

## 🐛 Troubleshooting

### Erro de encoding

Se houver erros de encoding ao ler CSVs, a função `carrega_dados()` já tenta múltiplos encodings automaticamente.

### Memória insuficiente

Use o modo `--rapido` para análises sem gráficos, economizando memória.

### Gráficos não aparecem

Certifique-se de que está em um ambiente com display gráfico. Em servidores sem GUI, use sempre `--salvar`.

## 📧 Suporte

Para questões ou suporte, consulte a documentação interna do projeto.

---

**Versão:** 1.0  
**Data:** Dezembro 2025
