# 📁 Índice de Arquivos - Projeto Análise Mari

Este documento lista e descreve todos os arquivos Python criados para hospedar as análises.

## 🐍 Arquivos Python Principais

### 1. **config.py**
- **Descrição:** Configurações globais do projeto
- **Conteúdo:**
  - Caminhos dos dados (2022, 2023, 2024)
  - Configurações de visualização
  - Cores das categorias
  - Ordens de exibição
  - Mapeamentos de dados
- **Uso:** Importado por todos os outros módulos
- **Personalização:** Ajuste os caminhos dos seus dados aqui

### 2. **utils.py**
- **Descrição:** Funções utilitárias reutilizáveis
- **Funções principais:**
  - `configurar_ambiente()` - Configuração inicial
  - `carrega_dados()` - Carrega CSVs
  - `preparar_dataframe()` - Limpa e transforma dados
  - `criar_subcategoria()` - Categoriza pacientes
  - `criar_categoria_urgenza()` - Mapeia códigos
  - `criar_features_temporais()` - Features de tempo
  - `criar_faixa_etaria()` - Faixas etárias
  - `plota_ausentes()` - Gráfico de missing values
- **Uso:** Base para todos os scripts de análise

### 3. **analise_urgenza.py**
- **Descrição:** Análises específicas de Categoria Urgenza
- **Funções principais:**
  - `estatisticas_urgenza()` - Estatísticas descritivas
  - `grafico_barras_urgenza()` - Gráficos de barras
  - `grafico_pizza_urgenza()` - Gráfico de pizza
  - `analise_urgenza_subgrupo()` - Análise cruzada
  - `heatmap_urgenza_subgrupo()` - Heatmap
  - `evolucao_temporal_urgenza()` - Série temporal
  - `analise_urgenza_idade()` - Por faixa etária
  - `resumo_executivo_urgenza()` - Resumo final
- **Uso:** Importado por main.py para análises de urgência

### 4. **analise_geral.py**
- **Descrição:** Análises complementares gerais
- **Funções principais:**
  - `analise_dimissione()` - Modalità Dimissione
  - `analise_problema_principal()` - Top problemas
  - `analise_pacientes_frequentes()` - Heavy users
  - `analise_temporal_geral()` - Análise temporal
  - `estatisticas_idade()` - Estatísticas de idade
  - `relatorio_geral()` - Relatório consolidado
- **Uso:** Análises adicionais conforme necessário

### 5. **main.py** ⭐
- **Descrição:** Script principal de execução
- **Funcionalidades:**
  - Carrega dados de todos os anos
  - Executa todas as análises
  - Gera gráficos
  - Salva resultados
- **Modos de execução:**
  - `python main.py` - Análise completa
  - `python main.py --rapido` - Só estatísticas
  - `python main.py --salvar ./output` - Salva gráficos
- **Uso:** Principal ponto de entrada para análises

### 6. **app.py** 🌐
- **Descrição:** API Flask para acesso web
- **Endpoints:**
  - `/` - Informações da API
  - `/status` - Status e dados carregados
  - `/analise/urgenza` - Análise de urgenza
  - `/analise/dimissione` - Análise de dimissione
  - `/analise/problemas` - Top problemas
  - `/analise/resumo` - Resumo geral
  - `/dados/filtrar` - Filtrar dados
  - `/dados/exportar/{formato}` - Exportar dados
  - `/recarregar` - Recarregar dados
- **Uso:** `python app.py` ou com Gunicorn
- **Porta:** 5000 (padrão)

### 7. **test_instalacao.py** ✅
- **Descrição:** Script de validação da instalação
- **Testes realizados:**
  1. Verificação de importações
  2. Verificação de módulos locais
  3. Verificação de configurações
  4. Teste de funções básicas
  5. Teste opcional com dados reais
- **Uso:** `python test_instalacao.py`
- **Quando usar:** Após instalação ou mudanças

## 📄 Arquivos de Documentação

### 8. **README.md** 📖
- **Descrição:** Documentação principal do projeto
- **Conteúdo:**
  - Estrutura do projeto
  - Como usar
  - Análises disponíveis
  - Configuração
  - Módulos detalhados
  - Hospedagem
  - Troubleshooting

### 9. **QUICKSTART.md** 🚀
- **Descrição:** Guia rápido de início (5 minutos)
- **Conteúdo:**
  - Instalação rápida
  - Comandos essenciais
  - Problemas comuns
  - Checklist de validação

### 10. **DEPLOY.md** 🌐
- **Descrição:** Guia completo de deploy em servidor
- **Conteúdo:**
  - Deploy em Linux
  - Configuração de produção
  - Nginx e Gunicorn
  - Systemd service
  - Docker (opcional)
  - Segurança
  - Monitoramento
  - Cron jobs

### 11. **EXEMPLOS_API.md** 💻
- **Descrição:** Exemplos de uso da API
- **Conteúdo:**
  - Exemplos com curl
  - Exemplos em Python
  - Exemplos em JavaScript
  - HTML + JavaScript
  - Dashboard simples
  - PowerShell (Windows)

### 12. **requirements.txt** 📦
- **Descrição:** Dependências do projeto
- **Pacotes principais:**
  - pandas, numpy (dados)
  - matplotlib, seaborn (visualização)
  - flask, gunicorn (API)
  - openpyxl (Excel)

### 13. **.gitignore** 🚫
- **Descrição:** Arquivos ignorados pelo Git
- **Ignora:**
  - Python cache
  - Ambientes virtuais
  - Dados CSV/Excel
  - Outputs e logs
  - IDEs

## 📊 Fluxo de Execução

### Modo Script (Análise Offline)

```
main.py
  ├── config.py (configurações)
  ├── utils.py
  │   ├── carrega_dados()
  │   └── preparar_dataframe()
  ├── analise_urgenza.py
  │   ├── estatisticas_urgenza()
  │   ├── grafico_barras_urgenza()
  │   ├── grafico_pizza_urgenza()
  │   └── ...
  └── analise_geral.py
      ├── analise_dimissione()
      └── ...
```

### Modo API (Servidor Web)

```
app.py
  ├── Flask (servidor web)
  ├── config.py
  ├── utils.py
  │   └── obter_dados() [cache]
  ├── analise_urgenza.py
  └── analise_geral.py
```

## 🎯 Qual Arquivo Usar?

### Para Análises Locais
→ Use **main.py**

### Para Servidor/API
→ Use **app.py**

### Para Testar Instalação
→ Use **test_instalacao.py**

### Para Ajustar Configurações
→ Edite **config.py**

### Para Adicionar Novas Análises
→ Edite **analise_geral.py** ou crie novo módulo

## 📝 Estrutura de Diretórios Recomendada

```
mari_doutorado/
├── analises/                    # Código Python
│   ├── config.py               # ← Ajuste caminhos aqui
│   ├── utils.py
│   ├── analise_urgenza.py
│   ├── analise_geral.py
│   ├── main.py                 # ← Execute este
│   ├── app.py                  # ← Ou este para API
│   ├── test_instalacao.py      # ← Teste primeiro
│   ├── requirements.txt
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── DEPLOY.md
│   ├── EXEMPLOS_API.md
│   └── .gitignore
├── dados/                       # Dados CSV
│   └── csv/
│       ├── 2022/
│       ├── 2023/
│       └── 2024/
├── output/                      # Gráficos salvos
└── venv/                        # Ambiente virtual
```

## 🔗 Dependências Entre Arquivos

```
config.py (base)
    ↓
utils.py (usa config)
    ↓
analise_urgenza.py (usa config + utils)
analise_geral.py (usa config + utils)
    ↓
main.py (usa todos acima)
app.py (usa todos acima)
```

## 📊 Análises Implementadas

### Categoria Urgenza ✅
- Distribuição e estatísticas
- Gráficos (barras, pizza)
- Análise por subgrupo
- Análise por faixa etária
- Evolução temporal
- Heatmaps
- Resumo executivo

### Análises Gerais ✅
- Modalità Dimissione
- Problema Principale
- Pacientes frequentes
- Análise temporal
- Estatísticas de idade
- Relatório consolidado

## 🚀 Comandos de Início Rápido

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Testar
python test_instalacao.py

# 3. Executar
python main.py

# 4. API (opcional)
python app.py
```

## 📚 Ordem de Leitura da Documentação

1. **QUICKSTART.md** - Para começar rápido
2. **README.md** - Documentação completa
3. **config.py** - Entender configurações
4. **EXEMPLOS_API.md** - Se usar API
5. **DEPLOY.md** - Para hospedar

## ✨ Recursos Especiais

- ✅ Cache de dados na API (performance)
- ✅ Múltiplos formatos de export (CSV, JSON, Excel)
- ✅ Filtros dinâmicos na API
- ✅ Gráficos personalizáveis
- ✅ Suporte a múltiplos encodings CSV
- ✅ Remoção automática de duplicatas
- ✅ Tratamento robusto de erros
- ✅ Logging e monitoramento
- ✅ Testes de validação

---

**Total de Arquivos Python:** 7  
**Total de Arquivos de Documentação:** 5  
**Total de Linhas de Código:** ~2500+  

**Status:** ✅ Pronto para produção
