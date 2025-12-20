"""
Configurações e constantes do projeto
"""

import os

# Caminhos dos dados
CAMINHO_BASE = "../dados/csv"
CAMINHO_2022 = "../dados/csv/2022"
CAMINHO_2023 = "../dados/csv/2023"
CAMINHO_2024 = "../dados/csv/2024"

# Configurações de visualização
FIGURA_TAMANHO = [22, 9]
FONTE_TAMANHO = 21
ESTILO_GRAFICO = "bmh"

# Cores para categorias de urgência
CORES_URGENZA = {
    "Bianca": "#E8E8E8",  # Branco/Cinza claro
    "Verde": "#2ECC71",  # Verde
    "Gialla": "#F1C40F",  # Amarelo
    "Arancione": "#E67E22",  # Laranja
    "Rossa": "#E74C3C",  # Vermelho
}

# Ordem das categorias de urgência (por gravidade)
ORDEM_URGENZA = ["Bianca", "Verde", "Gialla", "Arancione", "Rossa"]

# Ordem dos subgrupos de pacientes
ORDEM_SUBGRUPOS = ["Common user", "Frequent User", "Heavy User", "High User"]

# Ordem das faixas etárias
ORDEM_FAIXAS = ["15-44 anni", "45-64 anni", "> 64 anni"]

# Mapeamento de dias da semana
MAPEAMENTO_DIAS = {
    0: "Lunedì",
    1: "Martedì",
    2: "Mercoledì",
    3: "Giovedì",
    4: "Venerdì",
    5: "Sabato",
    6: "Domenica",
}

# Ordem dos dias da semana
ORDEM_DIAS = [
    "Lunedì",
    "Martedì",
    "Mercoledì",
    "Giovedì",
    "Venerdì",
    "Sabato",
    "Domenica",
]

# Colunas a serem removidas
COLUNAS_REMOVER = [
    "Fast Track",
    "Struttura",
    "Struttura di Ricovero/Trasferimento",
    "Sessione Ticket",
]
