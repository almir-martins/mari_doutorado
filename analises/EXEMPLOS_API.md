# Exemplos de Uso da API

Este documento contém exemplos de como usar a API Flask para acessar as análises.

## 🌐 Endpoints Disponíveis

### 1. Página Inicial e Informações

```bash
GET /
```

Retorna informações sobre a API e lista de endpoints disponíveis.

**Exemplo:**
```bash
curl http://localhost:5000/
```

**Resposta:**
```json
{
  "api": "Análise Mari Doutorado",
  "versao": "1.0",
  "endpoints": {
    "/status": "Status e informações básicas",
    "/analise/urgenza": "Estatísticas de Categoria Urgenza",
    ...
  }
}
```

### 2. Status da API

```bash
GET /status
```

Retorna informações sobre os dados carregados.

**Exemplo:**
```bash
curl http://localhost:5000/status
```

**Resposta:**
```json
{
  "status": "online",
  "registros_carregados": 121397,
  "pacientes_unicos": 64576,
  "periodo_inicio": "2022-08-01",
  "periodo_fim": "2024-12-31",
  "colunas": ["Urgenza", "Data Accesso", ...]
}
```

### 3. Análise de Categoria Urgenza

```bash
GET /analise/urgenza
```

Retorna estatísticas completas de Categoria Urgenza.

**Exemplo:**
```bash
curl http://localhost:5000/analise/urgenza
```

**Resposta:**
```json
{
  "status": "success",
  "distribuicao": {
    "contagem": {
      "Verde": 53052,
      "Bianco": 37815,
      "Arancione": 20677,
      "Rosso": 2670
    },
    "percentual": {
      "Verde": 46.45,
      "Bianco": 33.11,
      "Arancione": 18.10,
      "Rosso": 2.34
    }
  },
  "por_subgrupo": {...},
  "total_atendimentos": 121397,
  "pacientes_unicos": 64576
}
```

### 4. Análise de Modalità Dimissione

```bash
GET /analise/dimissione
```

Retorna estatísticas de tipos de alta.

**Exemplo:**
```bash
curl http://localhost:5000/analise/dimissione
```

### 5. Top Problemas Principais

```bash
GET /analise/problemas?top=10
```

Retorna os N problemas mais frequentes.

**Parâmetros:**
- `top`: Número de problemas a retornar (padrão: 10)

**Exemplo:**
```bash
curl "http://localhost:5000/analise/problemas?top=5"
```

### 6. Resumo Geral

```bash
GET /analise/resumo
```

Retorna um resumo consolidado de todas as análises.

**Exemplo:**
```bash
curl http://localhost:5000/analise/resumo
```

**Resposta:**
```json
{
  "status": "success",
  "dados_gerais": {
    "total_atendimentos": 121397,
    "pacientes_unicos": 64576,
    "media_atendimentos_paciente": 1.88,
    "periodo_inicio": "2022-08-01",
    "periodo_fim": "2024-12-31"
  },
  "categoria_urgenza": {
    "predominante": "Verde",
    "contagem": 53052,
    "percentual": 46.45
  },
  "subgrupos": {...},
  "faixas_etarias": {...}
}
```

### 7. Filtrar Dados

```bash
GET /dados/filtrar?categoria=Verde&ano=2023
```

Filtra dados por parâmetros específicos.

**Parâmetros disponíveis:**
- `categoria`: Categoria de urgenza (Bianco, Verde, Gialla, Arancione, Rosso)
- `ano`: Ano (2022, 2023, 2024)
- `subgrupo`: Subgrupo de pacientes

**Exemplos:**

```bash
# Filtrar por categoria Verde
curl "http://localhost:5000/dados/filtrar?categoria=Verde"

# Filtrar por ano 2023
curl "http://localhost:5000/dados/filtrar?ano=2023"

# Múltiplos filtros
curl "http://localhost:5000/dados/filtrar?categoria=Verde&ano=2023&subgrupo=Common%20user"
```

### 8. Exportar Dados

```bash
GET /dados/exportar/{formato}
```

Exporta dados em diferentes formatos.

**Formatos disponíveis:**
- `csv`: Arquivo CSV
- `json`: Formato JSON
- `excel`: Arquivo Excel

**Exemplos:**

```bash
# Exportar para CSV
curl "http://localhost:5000/dados/exportar/csv" -o dados.csv

# Exportar para JSON
curl "http://localhost:5000/dados/exportar/json" -o dados.json

# Exportar para Excel
curl "http://localhost:5000/dados/exportar/excel" -o dados.xlsx

# Exportar dados filtrados
curl "http://localhost:5000/dados/exportar/csv?categoria=Verde" -o dados_verde.csv
```

### 9. Recarregar Dados

```bash
GET /recarregar
```

Força o recarregamento dos dados do disco.

**Exemplo:**
```bash
curl http://localhost:5000/recarregar
```

## 🐍 Exemplos em Python

### Usando requests

```python
import requests
import pandas as pd

# URL base da API
BASE_URL = "http://localhost:5000"

# 1. Verificar status
response = requests.get(f"{BASE_URL}/status")
print(response.json())

# 2. Obter análise de urgenza
response = requests.get(f"{BASE_URL}/analise/urgenza")
dados_urgenza = response.json()
print(f"Total de atendimentos: {dados_urgenza['total_atendimentos']}")

# 3. Obter resumo
response = requests.get(f"{BASE_URL}/analise/resumo")
resumo = response.json()
print(f"Categoria predominante: {resumo['categoria_urgenza']['predominante']}")

# 4. Filtrar dados
params = {'categoria': 'Verde', 'ano': 2023}
response = requests.get(f"{BASE_URL}/dados/filtrar", params=params)
print(response.json())

# 5. Baixar dados em CSV
response = requests.get(f"{BASE_URL}/dados/exportar/csv")
with open('dados.csv', 'wb') as f:
    f.write(response.content)

# Ler o CSV
df = pd.read_csv('dados.csv')
print(df.head())

# 6. Obter dados em JSON
response = requests.get(f"{BASE_URL}/dados/exportar/json")
dados_json = response.json()
if dados_json['status'] == 'success':
    df = pd.DataFrame(dados_json['dados'])
    print(df.shape)
```

### Script de Monitoramento

```python
import requests
import time
from datetime import datetime

def monitorar_api(url, intervalo=300):
    """
    Monitora a API periodicamente
    
    Args:
        url: URL da API
        intervalo: Intervalo em segundos (padrão: 5 minutos)
    """
    while True:
        try:
            response = requests.get(f"{url}/status", timeout=10)
            data = response.json()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if data['status'] == 'online':
                print(f"[{timestamp}] ✓ API Online - {data['registros_carregados']} registros")
            else:
                print(f"[{timestamp}] ✗ API Offline")
        
        except requests.exceptions.RequestException as e:
            print(f"[{timestamp}] ✗ Erro: {e}")
        
        time.sleep(intervalo)

# Executar monitoramento
monitorar_api("http://localhost:5000")
```

### Dashboard Simples

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt

class DashboardMari:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def obter_resumo(self):
        """Obtém resumo da API"""
        response = requests.get(f"{self.api_url}/analise/resumo")
        return response.json()
    
    def plotar_urgenza(self):
        """Plota gráfico de categoria urgenza"""
        response = requests.get(f"{self.api_url}/analise/urgenza")
        data = response.json()
        
        categorias = list(data['distribuicao']['contagem'].keys())
        valores = list(data['distribuicao']['contagem'].values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(categorias, valores, color=['#E8E8E8', '#2ECC71', '#F1C40F', '#E67E22', '#E74C3C'])
        plt.title('Distribuição de Categoria Urgenza')
        plt.xlabel('Categoria')
        plt.ylabel('Frequência')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def imprimir_estatisticas(self):
        """Imprime estatísticas principais"""
        resumo = self.obter_resumo()
        
        print("="*60)
        print("DASHBOARD - ANÁLISE MARI DOUTORADO")
        print("="*60)
        
        dados_gerais = resumo['dados_gerais']
        print(f"\nTotal de Atendimentos: {dados_gerais['total_atendimentos']:,}")
        print(f"Pacientes Únicos: {dados_gerais['pacientes_unicos']:,}")
        print(f"Média Atend/Paciente: {dados_gerais['media_atendimentos_paciente']:.2f}")
        
        cat_urgenza = resumo['categoria_urgenza']
        print(f"\nCategoria Predominante: {cat_urgenza['predominante']}")
        print(f"  - Contagem: {cat_urgenza['contagem']:,}")
        print(f"  - Percentual: {cat_urgenza['percentual']:.2f}%")
        
        print("="*60)

# Usar dashboard
dash = DashboardMari("http://localhost:5000")
dash.imprimir_estatisticas()
dash.plotar_urgenza()
```

## 🌐 Exemplos em JavaScript

### Usando Fetch API

```javascript
// URL base
const BASE_URL = 'http://localhost:5000';

// Função auxiliar para fazer requisições
async function apiGet(endpoint) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// 1. Obter status
async function getStatus() {
    const data = await apiGet('/status');
    console.log('Status:', data);
}

// 2. Obter análise de urgenza
async function getUrgenzaAnalise() {
    const data = await apiGet('/analise/urgenza');
    console.log('Distribuição Urgenza:', data.distribuicao);
}

// 3. Obter resumo
async function getResumo() {
    const data = await apiGet('/analise/resumo');
    console.log('Resumo:', data);
}

// 4. Filtrar dados
async function filtrarDados(categoria, ano) {
    const params = new URLSearchParams({ categoria, ano });
    const data = await apiGet(`/dados/filtrar?${params}`);
    console.log('Dados filtrados:', data);
}

// Executar
getStatus();
getUrgenzaAnalise();
filtrarDados('Verde', 2023);
```

### HTML + JavaScript (Dashboard Simples)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Mari</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; }
        .stat { font-size: 24px; font-weight: bold; color: #2ECC71; }
    </style>
</head>
<body>
    <h1>Dashboard - Análise Mari</h1>
    
    <div class="card">
        <h2>Estatísticas Gerais</h2>
        <div id="stats"></div>
    </div>
    
    <div class="card">
        <h2>Categoria Urgenza</h2>
        <div id="urgenza"></div>
    </div>
    
    <script>
        const API_URL = 'http://localhost:5000';
        
        // Carregar estatísticas
        fetch(`${API_URL}/status`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('stats').innerHTML = `
                    <p>Total de Registros: <span class="stat">${data.registros_carregados.toLocaleString()}</span></p>
                    <p>Pacientes Únicos: <span class="stat">${data.pacientes_unicos.toLocaleString()}</span></p>
                    <p>Período: ${data.periodo_inicio} até ${data.periodo_fim}</p>
                `;
            });
        
        // Carregar análise de urgenza
        fetch(`${API_URL}/analise/urgenza`)
            .then(res => res.json())
            .then(data => {
                let html = '<table border="1"><tr><th>Categoria</th><th>Contagem</th><th>%</th></tr>';
                
                for (let cat in data.distribuicao.contagem) {
                    const count = data.distribuicao.contagem[cat];
                    const perc = data.distribuicao.percentual[cat];
                    html += `<tr><td>${cat}</td><td>${count.toLocaleString()}</td><td>${perc}%</td></tr>`;
                }
                
                html += '</table>';
                document.getElementById('urgenza').innerHTML = html;
            });
    </script>
</body>
</html>
```

## 🔍 Testando a API

### Usando curl (Linux/Mac)

```bash
# Status
curl http://localhost:5000/status | jq '.'

# Análise Urgenza
curl http://localhost:5000/analise/urgenza | jq '.distribuicao'

# Filtrar e salvar
curl "http://localhost:5000/dados/filtrar?categoria=Verde" | jq '.' > verde.json
```

### Usando PowerShell (Windows)

```powershell
# Status
Invoke-RestMethod -Uri "http://localhost:5000/status" | ConvertTo-Json

# Análise Urgenza
$response = Invoke-RestMethod -Uri "http://localhost:5000/analise/urgenza"
$response.distribuicao

# Baixar CSV
Invoke-WebRequest -Uri "http://localhost:5000/dados/exportar/csv" -OutFile "dados.csv"
```

---

**Nota:** Certifique-se de que a API está rodando antes de testar os exemplos!

Para iniciar a API:
```bash
python app.py
```
