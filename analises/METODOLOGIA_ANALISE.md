# Metodologia da Análise - Estudo de Frequentadores de Pronto Socorro

## Visão Geral do Estudo

Este documento descreve detalhadamente a metodologia, tecnologias, processos de limpeza e análises realizadas em um estudo sobre frequentadores de pronto socorro (PS) no período de 2022 a 2024, desenvolvido como parte de uma tese de doutorado.

---

## Objetivos da Análise

O estudo visa caracterizar e analisar o perfil de pacientes que utilizam serviços de pronto socorro, com foco especial em:

1. Identificar padrões de utilização do serviço
2. Categorizar pacientes por frequência de atendimento
3. Analisar características demográficas e clínicas
4. Avaliar urgência dos atendimentos
5. Compreender desfechos e modalidades de alta

---

## Tecnologias Utilizadas

### Linguagem de Programação
- **Python 3.x** - Linguagem principal para análise de dados

### Bibliotecas e Frameworks

#### Manipulação e Análise de Dados
- **Pandas** - Manipulação e análise de dados tabulares
- **NumPy** - Operações numéricas e matriciais

#### Visualização de Dados
- **Matplotlib** - Criação de gráficos e visualizações
- **Seaborn** - Visualizações estatísticas avançadas baseadas em Matplotlib

#### Utilidades
- **DateTime** - Manipulação de datas e horários
- **OS** - Operações com sistema de arquivos

### Ambiente de Desenvolvimento
- **Jupyter Notebook** - Ambiente interativo para análise exploratória de dados

---

## Estrutura dos Dados

### Fonte de Dados
- **Formato**: Arquivos CSV
- **Período**: 2022, 2023 e 2024
- **Estrutura**: Dados organizados por ano em diretórios separados

### Principais Variáveis Analisadas

#### Variáveis de Identificação
- `Numero Scheda PS`: Identificador único do atendimento
- `Paziente`: Nome do paciente
- `Data Accesso`: Data e hora de entrada no PS
- `Data Fine Contatto`: Data e hora de saída do PS
- `Data Nascita`: Data de nascimento do paciente

#### Variáveis Clínicas
- `Problema Principale`: Queixa principal do atendimento
- `Urgenza`: Código de urgência (1-4)
- `Categoria Urgenza`: Classificação de urgência (Rosso, Arancione, Verde, Bianco)
- `Modalità Dimissione`: Forma de alta do paciente

#### Variáveis Derivadas
- `Età`: Idade calculada em anos
- `Fascia d'età`: Faixa etária categorizada (15-44 anni, 45-64 anni, >64 anni)
- `Sottogruppo Pazienti`: Categoria de frequência de uso
- `Settimana`: Dia da semana do atendimento
- `Mese_anno`: Mês e ano do atendimento

---

## Processo de Limpeza e Exclusão de Dados

### 1. Carregamento e Consolidação dos Dados

#### Função `carrega_dados()`
- Leitura de múltiplos arquivos CSV de um diretório
- Tratamento de diferentes encodings (UTF-8, Latin-1, ISO-8859-1)
- Parsing automático de campos de data
- Concatenação de todos os arquivos
- Remoção de registros duplicados (mantendo primeira ocorrência)

### 2. Tratamento de Dados Faltantes

#### Colunas Removidas (>90% de dados faltantes)
- `Fast Track`
- `Struttura`
- `Struttura di Ricovero/Trasferimento`
- `Sessione Ticket`

#### Estratégia
- Análise visual da porcentagem de dados faltantes por coluna
- Exclusão de registros com valores ausentes nas colunas essenciais (`dropna()`)

### 3. Filtros de Exclusão Aplicados

#### 3.1. Filtros de Data e Idade
- **Datas de nascimento inválidas**: Exclusão de registros com `Data Nascita` 01/01/1900 com intuito de eliminar erros de digitação ou imputação de datas de nascimento genéricas.
- **Idade mínima**: Exclusão de pacientes com idade ≤ 14 anos (foco em adultos)

#### 3.2. Exclusão de Pacientes Específicos
Lista de 24 pacientes excluídos por inconsistências nos dados ou registros de teste:
```
- KAUR AMANDEEP
- KAUR HARPREET
- EL YAQOUTI MAJDA
- KAUR MANDEEP
- GUGA INDRIT
- SINGH SUKHWINDER
- BAHYOUNE ABDERRAHIM
- CITTASISS CENTO
- SABRI AHMED
- MUHAMMAD ZAHOOR
- KAUR MANPREET
- KAUR SANDEEP
- SINGH KARTAR
- SINGH TARSEM
- CITTASISS SEICENTOVENTI
- PROVA RICOVERODUE
- DISHA FIKE
- SINGH AMANDEEP
- KAUR BALJIT
- KAUR PARAMJIT
- (e outros registros de teste)
```

#### 3.3. Exclusão por Modalidade de Alta
Registros excluídos quando `Modalità Dimissione` ou `Problema Principale` igual a:
- "Il paziente abbandona il PS prima della visita medica"
- "Sintomi o disturbi ostetrico-ginecologici"
- "Inserito per errore"

#### 3.4. Remoção de Duplicatas
- Exclusão de registros duplicados por `Numero Scheda PS` (mantendo primeira ocorrência)

### 4. Transformações e Criações de Variáveis

#### 4.1. Cálculo de Idade
```python
Età = (Data Accesso - Data Nascita) / 365.25 dias
```

#### 4.2. Categorização de Urgência
Mapeamento do código numérico para categoria descritiva:
- 1 → Rosso (Vermelho - Emergência)
- 2 → Arancione (Laranja - Muito urgente)
- 3 → Verde (Verde - Pouco urgente)
- 4 → Bianco (Branco - Não urgente)

#### 4.3. Criação de Faixas Etárias
- **15-44 anni**: Adultos jovens e de meia-idade inicial
- **45-64 anni**: Meia-idade e pré-idosos
- **>64 anni**: Idosos

#### 4.4. Categorização de Subgrupos de Pacientes
Baseada na frequência total de atendimentos por paciente:
- **Common user**: < 4 atendimentos
- **Frequent User**: 4-5 atendimentos
- **High User**: 6-9 atendimentos
- **Heavy User**: ≥ 10 atendimentos

#### 4.5. Variáveis Temporais
- **Dia da semana**: Extração dos dias da semana
- **Mês/Ano**: Período mensal do atendimento

---

## Análises Realizadas

### 1. Análise Descritiva Básica

#### 1.1. Volumetria
- Total de atendimentos
- Número de pacientes únicos
- Número de cartões PS únicos
- Distribuição de cartões duplicados

#### 1.2. Estatísticas Descritivas
- **Variáveis numéricas**: Média, mediana, desvio padrão, mínimo, máximo
- **Variáveis categóricas**: Contagem de categorias únicas

### 2. Análise de Frequência de Uso

#### 2.1. Top Pacientes Mais Frequentes
- Identificação dos 10-20 pacientes com mais atendimentos
- Gráficos de barras horizontais com contagens
- Tabelas com nome e idade dos pacientes

#### 2.2. Distribuição por Subgrupo
- Contagem e percentual de atendimentos por subgrupo
- Contagem de pacientes únicos por subgrupo
- Visualizações:
  - Gráficos de barras comparativos
  - Gráficos de pizza
  - Análise de médias e desvios padrão

### 3. Análise Temporal

#### 3.1. Distribuição por Dia da Semana
- Contagem de atendimentos por dia
- Gráfico de barras com linha de média
- Identificação de picos e vales semanais

#### 3.2. Evolução Mensal
- Série temporal de atendimentos mês a mês
- Gráfico de linha com tendência
- Top 10 meses com maior volume
- Análise de sazonalidade

### 4. Análise Clínica

#### 4.1. Problemas de Saúde Principais
- Top 10 problemas mais frequentes
- Gráficos de barras e pizza
- Análise comparativa entre subgrupos
- Tabelas de frequência e percentual

#### 4.2. Categoria de Urgência
- Distribuição geral de urgências
- Análise cruzada: Urgência × Subgrupo de pacientes
- Análise cruzada: Urgência × Faixa etária
- Evolução temporal das urgências
- Heatmaps de distribuição
- Gráficos de barras agrupadas e empilhadas

### 5. Caracterização dos Subgrupos

#### 5.1. Caracterização Demográfica
- **Idade média por subgrupo**
  - Tabelas estatísticas (média, mediana, DP, mín, máx)
  - Gráficos de barras comparativos
  - Boxplots de distribuição

- **Faixas etárias por subgrupo**
  - Distribuição percentual
  - Gráficos empilhados
  - Gráficos de barras agrupadas

#### 5.2. Caracterização Clínica por Subgrupo
- **Modalità Dimissione**
  - Distribuição percentual por subgrupo
  - Gráficos de pizza individuais
  - Análise "Dimissione a domicilio" vs "Outras modalidades"
  
- **Problemas Principais**
  - Top 10 problemas por subgrupo
  - Grid de gráficos comparativos
  - Tabelas top 5 comparativas

#### 5.3. Análise de Pacientes Únicos
- Relação entre número de pacientes e volume de atendimentos
- Média de atendimentos por paciente em cada subgrupo
- Gráficos de pizza comparativos
- Análise de impacto no sistema de saúde

### 6. Análises Cruzadas Avançadas

#### 6.1. Tabelas de Contingência
- Categoria Urgenza × Sottogruppo Pazienti
- Categoria Urgenza × Fascia d'età
- Categoria Urgenza × Modalità Dimissione

#### 6.2. Visualizações Multidimensionais
- Heatmaps de correlação
- Gráficos de barras empilhadas normalizadas
- Gráficos de barras agrupadas por múltiplas variáveis

---

## Tipos de Visualizações Utilizadas

### Gráficos Estatísticos
1. **Gráficos de Barras**
   - Horizontais e verticais
   - Simples, agrupados e empilhados
   - Com anotações de valores e linhas de média

2. **Gráficos de Pizza**
   - Distribuições percentuais
   - Comparações entre categorias
   - Com explosão de fatias para destaque

3. **Gráficos de Linha**
   - Séries temporais
   - Evolução de múltiplas categorias
   - Com marcadores e grades

4. **Boxplots**
   - Distribuição de variáveis numéricas
   - Comparação entre grupos
   - Identificação de outliers

5. **Heatmaps**
   - Correlações entre variáveis categóricas
   - Análises de tabelas cruzadas
   - Gradientes de cores para facilitar interpretação

### Elementos Visuais Adicionados
- Valores numéricos sobre barras
- Linhas de referência (médias)
- Grades de fundo
- Legendas descritivas
- Títulos informativos em italiano
- Paletas de cores temáticas e intuitivas

---

## Configurações de Visualização

### Estilo e Aparência
- **Estilo base**: 'bmh' (Bayesian Methods for Hackers)
- **Tamanho padrão de figura**: 22×9 polegadas
- **Tamanho de fonte**: 21pt (base)
- **Seaborn**: Configurações padrão aplicadas

### Paletas de Cores
- **Subgrupos de usuários**:
  - Common user: Verde (#2ecc71)
  - Frequent User: Azul (#3498db)
  - High User: Laranja (#f39c12)
  - Heavy User: Vermelho (#e74c3c)

- **Categorias de urgência**:
  - Bianco: Cinza claro (#A1A1A1)
  - Verde: Verde (#2ECC71)
  - Gialla: Amarelo (#F1C40F)
  - Arancione: Laranja (#E67E22)
  - Rosso: Vermelho (#E74C3C)

---

## 🔍 Função de Apoio Principais

### 1. `jupyter_settings()`
Configuração inicial do ambiente:
- Supressão de warnings
- Configuração de matplotlib inline
- Definição de estilo e tamanho padrão
- Configurações de exibição do Pandas

### 2. `exibe_boxplot()` e `exibe_countplot()`
Funções para plotagem rápida de múltiplos gráficos lado a lado

### 3. `plota_ausentes()`
Análise visual de dados faltantes:
- Tabela de contagem
- Gráfico de barras com percentuais
- Filtro por percentual mínimo

### 4. `carrega_dados()`
Carregamento robusto de dados:
- Múltiplos arquivos
- Tratamento de encoding
- Parsing de datas
- Remoção de duplicatas

### 5. `subcategoria()`
Categorização de pacientes por frequência de uso

### 6. `filtra_pacientes()`
Aplicação de todos os filtros de exclusão:
- Idades inválidas
- Pacientes específicos
- Modalidades de alta
- Duplicatas

### 7. `agrupa()` e `plota_mais_frequentes()`
Identificação e visualização de pacientes mais frequentes

---

## Insights e Métricas Calculadas

### Métricas de Frequência
- Contagens absolutas e percentuais
- Médias e medianas por grupo
- Desvios padrão
- Valores acumulados

### Análises Comparativas
- Diferenças entre grupos
- Proporções relativas
- Rankings (top N)
- Distribuições percentuais dentro de categorias

### Indicadores de Impacto
- Percentual de pacientes heavy users
- Percentual de atendimentos gerados por cada subgrupo
- Média de atendimentos por paciente
- Concentração de uso do serviço

---

## Considerações Finais

### Pontos Fortes da Metodologia
1. **Robustez no carregamento de dados**: Tratamento de múltiplos encodings
2. **Limpeza criteriosa**: Filtros bem definidos e documentados
3. **Categorização clinicamente relevante**: Subgrupos baseados em literatura
4. **Visualizações informativas**: Múltiplos ângulos de análise
5. **Reprodutibilidade**: Código modular e bem estruturado

### Limitações
1. Dados limitados a 3 anos (2022-2024)
2. Análise focada em variáveis disponíveis no sistema
3. Possível subnotificação em algumas variáveis
4. Exclusão necessária de registros incompletos pode introduzir viés

### Aplicações dos Resultados
- Planejamento de recursos em pronto socorro
- Identificação de pacientes de alto risco
- Desenvolvimento de estratégias de prevenção
- Otimização de fluxos de atendimento
- Políticas de saúde pública baseadas em evidências

---

## Estrutura do Código

O notebook está organizado em seções hierárquicas:

### STEP 0 - Preparação
- 0.1. Imports
- 0.2. Funções de apoio
- 0.3. Carregamento dos dados

### 1 - Entendimento dos Dados
- 1.1. Renomeação de colunas
- 1.2. Volumetria
- 1.3. Tipos de dados
- 1.4. Alteração de tipos
- 1.5. Verificação de dados faltantes
- 1.7. Estatística descritiva
- 1.8. Aplicação de filtros

### 2 - Análise Exploratória dos Dados
- 2.1. Análise univariada
- 2.2. Análise bivariada
  - Pacientes mais frequentes
  - Atendimentos por dia da semana
  - Principais problemas de saúde
  - Atendimentos por mês
  - Categorias de usuários

### 3 - Caracterização Detalhada dos Subgrupos
- 3.1. Caracterização por faixas etárias
- 3.2. Idade média por subgrupo
- 3.3. Caracterização por modalità dimissione
- 3.4. Caracterização por problema principale
- 3.5. Relação subgrupo/número total de pacientes

### 4 - Análise de Categoria Urgenza
- Visão geral e estatísticas descritivas
- Distribuições e gráficos
- Análises cruzadas com múltiplas variáveis
- Análise temporal
- Resumos e insights finais

---

## Data de Última Atualização
30 de dezembro de 2025

---

## Contexto Acadêmico
Este estudo faz parte de uma pesquisa de doutorado focada na caracterização e compreensão do perfil de usuários frequentes de serviços de emergência, com objetivo de contribuir para o desenvolvimento de estratégias de gestão e cuidado mais eficientes no sistema de saúde.
